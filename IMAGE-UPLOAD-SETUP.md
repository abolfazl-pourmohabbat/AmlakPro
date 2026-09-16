# AmlakPro — Image Upload on Vercel

Vercel Functions use a read-only deployment filesystem, so Django's default `FileSystemStorage` cannot persist uploaded property/agent images. AmlakPro now switches its media storage to **Vercel Blob** whenever `BLOB_READ_WRITE_TOKEN` is present.

## One-time Vercel setup

1. Open the **`amlakpro-api`** Vercel project (the Django backend project).
2. Open **Storage**.
3. Choose **Create Database → Blob**.
4. Choose **Public** storage because property/agent images are public website media.
5. Connect the Blob store to the `amlakpro-api` project and enable it for **Production** (and Preview if desired).
6. Vercel adds `BLOB_READ_WRITE_TOKEN` to the project environment automatically.
7. Redeploy the backend.

After redeployment, the existing Django admin upload fields for property and agent images continue to work. The files are stored in Vercel Blob instead of `/var/task/media`.

## Upload limit

The admin currently limits images to **4 MB**. This leaves headroom under Vercel's 4.5 MB Function request-body limit for the multipart request.
