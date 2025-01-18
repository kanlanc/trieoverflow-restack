from restack_ai.function import function, log
from pydantic import BaseModel


@function.defn()
async def perplexityAgent() -> str:
    try:
        log.info("perplexityAgent function started")

        perplexityMessage = """The code snippet shown has syntax errors and won't work as intended. Here's the correct way to use the AssemblyScript loader:
javascript
import loader from "@assemblyscript/loader";

const instance = await loader.instantiateStreaming(
  fetch("./build/debug.wasm"),
  { /* imports if needed */ }
);

const exports = instance.exports;
A few key points about using AssemblyScript loader:
The loader has been deprecated in AssemblyScript 0.20 and newer versions10. It's recommended to use static bindings generation instead.
If streaming instantiation is not available, you can use the standard instantiate method:
javascript
const instance = await loader.instantiate(
  await fetch("./build/debug.wasm"), 
  { /* imports if needed */ }
);
For Node.js environments, you can load from the filesystem:
javascript
import fs from 'node:fs';
const instance = await loader.instantiate(
  fs.readFileSync("./build/debug.wasm"),
  { /* imports if needed */ }
);"""
        return perplexityMessage

    except Exception as e:
        log.error("perplexityAgent function failed", error=e)
        raise e
