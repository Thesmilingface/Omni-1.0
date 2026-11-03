use eframe::egui;
use serde::{Deserialize, Serialize};
use std::sync::mpsc::{self, Receiver, Sender};
use std::thread;

const API: &str = "http://127.0.0.1:8765";

#[derive(Serialize)]
struct ChatRequest<'a> { conversation_id: &'a str, message: &'a str }
#[derive(Deserialize)]
struct ChatResponse { reply: String }

struct SmerkaApp {
    input: String,
    transcript: Vec<(bool, String)>,
    tx: Sender<Result<String, String>>,
    rx: Receiver<Result<String, String>>,
    busy: bool,
    start: std::time::Instant,
}

impl Default for SmerkaApp {
    fn default() -> Self {
        let (tx, rx) = mpsc::channel();
        Self { input: String::new(), transcript: Vec::new(), tx, rx, busy: false, start: std::time::Instant::now() }
    }
}

impl SmerkaApp {
    fn send(&mut self) {
        let text = self.input.trim().to_owned();
        if text.is_empty() || self.busy { return; }
        self.transcript.push((true, text.clone()));
        self.input.clear();
        self.busy = true;
        let tx = self.tx.clone();
        thread::spawn(move || {
            let result = (|| -> Result<String, String> {
                let client = reqwest::blocking::Client::builder().timeout(std::time::Duration::from_secs(60)).build().map_err(|_| "Could not initialize HTTP client".to_owned())?;
                let response = client.post(format!("{API}/chat")).json(&ChatRequest { conversation_id: "desktop_default", message: &text }).send().map_err(|_| "Cannot reach SMERKA service. Start `python -m smerka_service` first.".to_owned())?;
                let status = response.status();
                if !status.is_success() {
                    let body = response.text().unwrap_or_default();
                    let detail = serde_json::from_str::<serde_json::Value>(&body).ok().and_then(|v| v.get("detail").and_then(|d| d.as_str()).map(str::to_owned)).unwrap_or_else(|| format!("Service returned HTTP {status}"));
                    return Err(detail);
                }
                response.json::<ChatResponse>().map(|r| r.reply).map_err(|_| "Service returned an invalid response".to_owned())
            })();
            let _ = tx.send(result);
        });
    }
}

impl eframe::App for SmerkaApp {
    fn update(&mut self, ctx: &egui::Context, _frame: &mut eframe::Frame) {
        while let Ok(result) = self.rx.try_recv() {
            self.busy = false;
            match result { Ok(text) => self.transcript.push((false, text)), Err(error) => self.transcript.push((false, format!("Error: {error}"))) }
        }
        ctx.request_repaint_after(std::time::Duration::from_millis(32));
        egui::CentralPanel::default().frame(egui::Frame::new().fill(egui::Color32::from_rgb(16, 19, 26))).show(ctx, |ui| {
            ui.horizontal(|ui| {
                ui.vertical(|ui| {
                    ui.heading(egui::RichText::new("SMERKA").color(egui::Color32::from_rgb(130, 205, 235)));
                    ui.label(egui::RichText::new("PERSONAL ASSISTANT · LOCAL DESKTOP").small().color(egui::Color32::GRAY));
                });
                ui.with_layout(egui::Layout::right_to_left(egui::Align::Center), |ui| {
                    ui.label(if self.busy { "● THINKING" } else { "● READY" });
                });
            });
            ui.separator();
            ui.columns(2, |cols| {
                let (chat, companion) = cols.split_at_mut(1);
                chat[0].vertical(|ui| {
                    ui.heading("Conversation");
                    egui::ScrollArea::vertical().stick_to_bottom(true).max_height(ui.available_height() - 115.0).show(ui, |ui| {
                        for (is_user, text) in &self.transcript {
                            let label = if *is_user { "YOU" } else { "SMERKA" };
                            ui.group(|ui| { ui.label(egui::RichText::new(label).small().strong().color(if *is_user { egui::Color32::LIGHT_BLUE } else { egui::Color32::from_rgb(195, 155, 240) })); ui.label(text); });
                            ui.add_space(6.0);
                        }
                    });
                    ui.add_space(8.0);
                    let response = ui.add(egui::TextEdit::multiline(&mut self.input).hint_text("Message SMERKA… (Ctrl+Enter to send)").desired_rows(3));
                    let enter = response.has_focus() && ui.input(|i| i.modifiers.ctrl && i.key_pressed(egui::Key::Enter));
                    ui.horizontal(|ui| {
                        ui.label("Provider keys stay in the local Python service environment.");
                        if ui.add_enabled(!self.busy, egui::Button::new(if self.busy { "Working…" } else { "Send" })).clicked() || enter { self.send(); }
                    });
                });
                companion[0].vertical_centered(|ui| {
                    ui.heading("Companion");
                    ui.label("Procedural 2D preview");
                    let (rect, _) = ui.allocate_exact_size(egui::vec2(ui.available_width().min(330.0), ui.available_height().min(360.0)), egui::Sense::hover());
                    let painter = ui.painter_at(rect);
                    let center = rect.center();
                    let t = self.start.elapsed().as_secs_f32();
                    let bob = if self.busy { (t * 2.8).sin() * 5.0 } else { (t * 1.15).sin() * 2.0 };
                    let head = egui::pos2(center.x, center.y - 20.0 + bob);
                    painter.circle_filled(egui::pos2(center.x, center.y + 110.0), 82.0, egui::Color32::from_rgb(37, 46, 61));
                    painter.circle_filled(head, 74.0, egui::Color32::from_rgb(229, 193, 169));
                    painter.circle_filled(egui::pos2(head.x - 26.0, head.y - 13.0), 5.0, egui::Color32::from_rgb(32, 38, 49));
                    painter.circle_filled(egui::pos2(head.x + 26.0, head.y - 13.0), 5.0, egui::Color32::from_rgb(32, 38, 49));
                    let mouth = if self.busy { 7.0 } else { 2.0 + (t * 2.0).sin().abs() * 2.0 };
                    painter.line_segment([egui::pos2(head.x - 10.0, head.y + 24.0), egui::pos2(head.x + 10.0, head.y + 24.0 + mouth)], egui::Stroke::new(2.5, egui::Color32::from_rgb(120, 64, 69)));
                    ui.label(if self.busy { "Thinking…" } else { "Here with you" });
                    ui.label(egui::RichText::new("Not a Live2D model; no audio sync yet.").small().color(egui::Color32::GRAY));
                });
            });
        });
    }
}

fn main() -> eframe::Result<()> {
    let options = eframe::NativeOptions { viewport: egui::ViewportBuilder::default().with_inner_size([1050.0, 720.0]).with_min_inner_size([780.0, 560.0]), ..Default::default() };
    eframe::run_native("SMERKA AI", options, Box::new(|_| Ok(Box::<SmerkaApp>::default())))
}
