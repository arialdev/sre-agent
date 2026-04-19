"use server";

import { redirect } from "next/navigation";
import { revalidatePath } from "next/cache";

import { parseRunbookMutationFormData } from "@/src/lib/runbooks/input";
import { getRunbookServices } from "@/src/lib/runbooks/container";

export async function createRunbookAction(formData: FormData): Promise<void> {
  const input = await parseRunbookMutationFormData(formData);
  const services = getRunbookServices();
  await services.management.createRunbook(input);
  revalidatePath("/");
  redirect("/");
}

export async function createRunbookVersionAction(
  formData: FormData,
): Promise<void> {
  const runbookId = String(formData.get("runbookId") || "");
  if (!runbookId) {
    throw new Error("A runbook id is required");
  }

  const input = await parseRunbookMutationFormData(formData);
  const services = getRunbookServices();
  await services.management.createVersion(runbookId, input);
  revalidatePath("/");
  redirect("/");
}

export async function publishRunbookVersionAction(
  formData: FormData,
): Promise<void> {
  const runbookId = String(formData.get("runbookId") || "");
  const versionId = String(formData.get("versionId") || "");

  if (!runbookId || !versionId) {
    throw new Error("Runbook id and version id are required");
  }

  const services = getRunbookServices();
  await services.management.publishVersion(runbookId, versionId);
  revalidatePath("/");
  redirect("/");
}
