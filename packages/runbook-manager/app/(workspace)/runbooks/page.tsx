import Link from "next/link";
import { getRunbookServices } from "@/src/lib/runbooks/container";

function formatDate(value: string): string {
  return new Intl.DateTimeFormat("en", {
    dateStyle: "medium",
    timeStyle: "short",
  }).format(new Date(value));
}

export default async function RunbooksPage() {
  const services = getRunbookServices();
  const runbooks = await services.management.listRunbooks();

  return (
    <section className="page-section">
      <div className="page-header page-header--centered">
        <div className="page-header__content">
          <h1>Runbook library</h1>
          <p className="page-copy">
            Browse the library, open any runbook in its own view, and add new runbooks
            whenever your team needs them.
          </p>
        </div>
      </div>

      <div className="stats-grid">
        <article className="metric-card">
          <span>Total runbooks</span>
          <strong>{runbooks.length}</strong>
        </article>
        <article className="metric-card">
          <span>Tagged runbooks</span>
          <strong>{runbooks.filter((runbook) => runbook.tags.length > 0).length}</strong>
        </article>
        <article className="metric-card">
          <span>Newest update</span>
          <strong>{runbooks[0] ? formatDate(runbooks[0].updatedAt).split(",")[0] : "None"}</strong>
        </article>
      </div>

      <section className="panel panel-library">
          <div className="panel-header panel-header--stack-mobile">
          <div className="panel-header">
            <div>
              <p className="eyebrow">Library</p>
              <h2>Browse runbooks</h2>
            </div>
          </div>
          <Link className="button-link" href="/runbooks/new">
            New
          </Link>
        </div>

          {runbooks.length === 0 ? (
            <article className="empty-state">
              <h3>No runbooks yet</h3>
              <p>
                Create the first runbook from the publish page. It will be indexed
                and opened in its dedicated view as soon as it is created.
              </p>
            </article>
          ) : (
            <div className="runbook-list">
              {runbooks.map((runbook) => {
                return (
                  <Link
                    className="runbook-list-item"
                    href={`/runbooks/${runbook.id}`}
                    key={runbook.id}
                  >
                    <div className="runbook-list-item__header">
                      <div>
                        <h3>{runbook.title}</h3>
                      </div>
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

                    <div className="meta-row">
                      <span>Created {formatDate(runbook.createdAt)}</span>
                      <span>{runbook.sourceFilename}</span>
                      <span>Updated {formatDate(runbook.updatedAt)}</span>
                    </div>
                  </Link>
                );
              })}
            </div>
          )}
      </section>
    </section>
  );
}
