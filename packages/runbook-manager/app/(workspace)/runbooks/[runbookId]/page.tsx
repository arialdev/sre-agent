import Link from "next/link";
import { notFound } from "next/navigation";

import { deleteRunbookAction } from "@/app/actions";
import { DeleteRunbookDialog } from "@/app/_components/delete-runbook-dialog";
import { getRunbookServices } from "@/src/lib/runbooks/container";

function formatDate(value: string): string {
  return new Intl.DateTimeFormat("en", {
    dateStyle: "medium",
    timeStyle: "short",
  }).format(new Date(value));
}

type RunbookDetailPageProps = {
  params: Promise<{ runbookId: string }>;
};

export default async function RunbookDetailPage({
  params,
}: RunbookDetailPageProps) {
  const { runbookId } = await params;
  const services = getRunbookServices();
  const detail = await services.management.getRunbookDetail(runbookId);

  if (!detail) {
    notFound();
  }

  const { runbook, content } = detail;

  return (
    <section className="page-section">
      <div className="page-header page-header--detail page-header--centered">
        <div className="page-header__content">
          <Link className="back-link" href="/runbooks">
            Back to library
          </Link>
          <p className="eyebrow">Runbook detail</p>
          <h1>{runbook.title}</h1>
          <p className="page-copy">
            Read the stored markdown content and manage deletion from this dedicated view.
          </p>
        </div>
        <div className="page-header-actions">
          <DeleteRunbookDialog
            action={deleteRunbookAction}
            runbookId={runbook.id}
            runbookSlug={runbook.slug}
            runbookTitle={runbook.title}
          />
        </div>
      </div>

      <article className="panel detail-panel">
        <div className="panel-header">
          <div>
            <p className="eyebrow">Markdown content</p>
            <h2>{runbook.title}</h2>
          </div>
        </div>

        <div className="meta-row">
          <span>{runbook.sourceFilename}</span>
          <span>Created {formatDate(runbook.createdAt)}</span>
          <span>Updated {formatDate(runbook.updatedAt)}</span>
        </div>

        {runbook.tags.length > 0 ? (
          <div className="badge-row">
            {runbook.tags.map((tag) => (
              <span className="badge" key={`${runbook.id}-${tag}`}>
                {tag}
              </span>
            ))}
          </div>
        ) : null}

        <pre className="markdown-view">{content}</pre>
      </article>
    </section>
  );
}
