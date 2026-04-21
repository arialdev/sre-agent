"use server";

import { redirect } from "next/navigation";
import { revalidatePath } from "next/cache";

import { parseRunbookMutationFormData } from "@/src/lib/runbooks/input";
import { getRunbookServices } from "@/src/lib/runbooks/container";

export async function createRunbookAction(formData: FormData): Promise<void> {
  const input = await parseRunbookMutationFormData(formData);
  const services = getRunbookServices();
  const runbook = await services.management.createRunbook(input);
  revalidatePath("/runbooks");
  revalidatePath(`/runbooks/${runbook.id}`);
  redirect(`/runbooks/${runbook.id}`);
}

export async function deleteRunbookAction(
  formData: FormData,
): Promise<void> {
  const runbookId = String(formData.get("runbookId") || "");
  const confirmationSlug = String(formData.get("confirmationSlug") || "");

  if (!runbookId) {
    throw new Error("Runbook id is required");
  }

  const services = getRunbookServices();
  const runbook = await services.management.getRunbook(runbookId);

  if (!runbook) {
    throw new Error("Runbook was not found");
  }

  if (confirmationSlug !== runbook.slug) {
    throw new Error("Runbook slug confirmation does not match");
  }

  await services.management.deleteRunbook(runbookId);
  revalidatePath("/runbooks");
  redirect("/runbooks");
}
