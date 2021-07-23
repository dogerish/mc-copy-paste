from utils import log

def write(ctx: dict, filename: str) -> None:
    filename = "sels/" + filename
    log(ctx["mc"], f"Saving selection to '{filename}'")
    ctx["sel"].write(filename)
    log(ctx["mc"], f"Saved.")
