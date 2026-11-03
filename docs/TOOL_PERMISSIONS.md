# Tool permissions

A Python `Workspace` helper confines file reads and writes to the configured workspace and enforces a size limit. It is a library integration point, not yet exposed as an AI-callable tool. The service intentionally does not offer arbitrary shell execution, OS automation, or destructive operations. Add explicit approval and auditing before exposing write tools through the UI.
