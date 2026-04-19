import { NextResponse } from "next/server";

import { getRunbookServices } from "@/src/lib/runbooks/container";
import { parseRunbookMutationFormData } from "@/src/lib/runbooks/input";

export async function GET() {
  const services = getRunbookServices();
  const runbooks = await services.management.listRunbooks();
  return NextResponse.json({ runbooks });
}

export async function POST(request: Request) {
  const formData = await request.formData();
  const input = await parseRunbookMutationFormData(formData);
  const services = getRunbookServices();
  const runbook = await services.management.createRunbook(input);
  return NextResponse.json({ runbook }, { status: 201 });
}
