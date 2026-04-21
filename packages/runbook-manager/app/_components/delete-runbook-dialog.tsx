"use client";

import { useEffect, useRef, useState } from "react";

type DeleteRunbookDialogProps = {
  action: (formData: FormData) => Promise<void>;
  runbookId: string;
  runbookSlug: string;
  runbookTitle: string;
};

export function DeleteRunbookDialog({
  action,
  runbookId,
  runbookSlug,
  runbookTitle,
}: DeleteRunbookDialogProps) {
  const dialogRef = useRef<HTMLDialogElement>(null);
  const [confirmationSlug, setConfirmationSlug] = useState("");

  useEffect(() => {
    const dialog = dialogRef.current;
    if (!dialog) {
      return;
    }

    const handleClose = () => setConfirmationSlug("");
    dialog.addEventListener("close", handleClose);
    return () => dialog.removeEventListener("close", handleClose);
  }, []);

  return (
    <>
      <button
        className="button-danger"
        onClick={() => dialogRef.current?.showModal()}
        type="button"
      >
        Delete runbook
      </button>

      <dialog className="confirm-dialog" ref={dialogRef}>
        <form action={action} className="confirm-dialog__body">
          <div className="confirm-dialog__copy">
            <p className="eyebrow">Permanent deletion</p>
            <h2>Delete {runbookTitle}?</h2>
            <p>
              This removes the runbook metadata, stored markdown, and indexed
              knowledge. To confirm, type the runbook slug below.
            </p>
            <code className="confirm-dialog__id">{runbookSlug}</code>
          </div>

          <input name="runbookId" type="hidden" value={runbookId} />

          <label>
            Confirm runbook slug
            <input
              name="confirmationSlug"
              onChange={(event) => setConfirmationSlug(event.target.value)}
              placeholder={runbookSlug}
              value={confirmationSlug}
            />
          </label>

          <div className="confirm-dialog__actions">
            <button
              onClick={() => dialogRef.current?.close()}
              type="button"
            >
              Cancel
            </button>
            <button
              className="button-danger"
              disabled={confirmationSlug !== runbookSlug}
              type="submit"
            >
              Delete permanently
            </button>
          </div>
        </form>
      </dialog>
    </>
  );
}
