---
layout: docs
---

# FAQ


## When importing a Zip, Tar, or Tar.GZ file from a remote location, it is automatically exploded?

Yes. The tool automatically explodes any archive into the target location.

## When importing are files and directories overwritten?

The current design is to fail if a target location exists.  In the future, an overwrite option may be added,
but the default behavior will remain the same.


