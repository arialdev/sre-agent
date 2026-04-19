import {
  createRunbookAction,
  createRunbookVersionAction,
  publishRunbookVersionAction,
} from "@/app/actions";
import { getRunbookServices } from "@/src/lib/runbooks/container";

function formatDate(value: string): string {
  return new Intl.DateTimeFormat("en", {
    dateStyle: "medium",
    timeStyle: "short",
  }).format(new Date(value));
}

export default async function HomePage() {
  const services = getRunbookServices();
  const runbooks = await services.management.listRunbooks();
  const publishedRunbooks = runbooks.filter((runbook) => runbook.activeVersionId).length;
  const indexedVersions = runbooks.flatMap((runbook) => runbook.versions).filter(
    (version) => version.ingestionStatus === "indexed",
  ).length;

  return (
    <main>
      <section className="hero">
        <div>
          <p className="muted">Runbook management platform</p>
          <h1>Operate the knowledge base without binding the agent to repo fixtures.</h1>
        </div>
        <p>
          This fullstack app manages runbooks, versions, publication and retrieval.
          The current adapters are local on purpose: the domain is already separated
          from infrastructure so Azure and AWS can arrive later without rewriting the
          business rules.
        </p>
        <div className="hero-grid">
          <article className="stat-card">
            <span>Runbooks</span>
            <strong>{runbooks.length}</strong>
          </article>
          <article className="stat-card">
            <span>Published</span>
            <strong>{publishedRunbooks}</strong>
          </article>
          <article className="stat-card">
            <span>Indexed versions</span>
            <strong>{indexedVersions}</strong>
          </article>
        </div>
      </section>

      <section className="layout-grid">
        <aside className="panel">
          <h2>Create a runbook</h2>
          <p>
            Upload a Markdown file or paste the content directly. New versions are
            indexed automatically and stay as drafts until published.
          </p>
          <form action={createRunbookAction} encType="multipart/form-data">
            <label>
              Title
              <input name="title" placeholder="Redis cache eviction" required />
            </label>
            <label>
              Summary
              <input
                name="summary"
                placeholder="Symptoms, diagnosis and recovery steps"
                required
              />
            </label>
            <label>
              Tags
              <input
                name="tags"
                placeholder="redis, cache, eviction"
                required
              />
            </label>
            <label>
              Markdown file
              <input name="file" type="file" accept=".md,text/markdown" />
            </label>
            <label>
              Or paste Markdown
              <textarea
                name="content"
                placeholder={"# Summary\n\n## Symptoms\n- ...\n\n## Diagnosis\n- ..."}
              />
            </label>
            <button type="submit">Create runbook</button>
          </form>
        </aside>

        <section className="runbooks">
          {runbooks.length === 0 ? (
            <article className="runbook-card">
              <h2>No runbooks yet</h2>
              <p>
                Create the first runbook from the panel on the left. It will be stored
                locally and indexed immediately through the inline coordinator.
              </p>
            </article>
          ) : null}

          {runbooks.map((runbook) => (
            <article className="runbook-card" key={runbook.id}>
              <div className="runbook-header">
                <div>
                  <p className="muted">{runbook.slug}</p>
                  <h2>{runbook.title}</h2>
                  <p>{runbook.summary}</p>
                </div>
                <div className="badge-row">
                  {runbook.tags.map((tag) => (
                    <span className="badge" key={`${runbook.id}-${tag}`}>
                      {tag}
                    </span>
                  ))}
                  {runbook.activeVersionId ? (
                    <span className="badge">published</span>
                  ) : (
                    <span className="badge warning">draft-only</span>
                  )}
                </div>
              </div>

              <div className="meta">
                <span>Created {formatDate(runbook.createdAt)}</span>
                <span>Updated {formatDate(runbook.updatedAt)}</span>
                <span>{runbook.versions.length} versions</span>
              </div>

              <div className="panel" style={{ marginTop: "1rem" }}>
                <h2>Add a version</h2>
                <form action={createRunbookVersionAction} encType="multipart/form-data">
                  <input name="runbookId" type="hidden" value={runbook.id} />
                  <label>
                    Title
                    <input defaultValue={runbook.title} name="title" required />
                  </label>
                  <label>
                    Summary
                    <input defaultValue={runbook.summary} name="summary" required />
                  </label>
                  <label>
                    Tags
                    <input defaultValue={runbook.tags.join(", ")} name="tags" required />
                  </label>
                  <label>
                    Markdown file
                    <input name="file" type="file" accept=".md,text/markdown" />
                  </label>
                  <label>
                    Or paste Markdown
                    <textarea
                      name="content"
                      placeholder="Paste a revised runbook version here"
                    />
                  </label>
                  <button className="secondary" type="submit">
                    Add version
                  </button>
                </form>
              </div>

              <div className="version-list" style={{ marginTop: "1rem" }}>
                {runbook.versions
                  .slice()
                  .sort((left, right) => right.versionNumber - left.versionNumber)
                  .map((version) => (
                    <section className="version-card" key={version.id}>
                      <div className="runbook-header">
                        <div>
                          <strong>Version {version.versionNumber}</strong>
                          <p>{version.summary}</p>
                        </div>
                        <div className="badge-row">
                          <span className="badge">{version.publicationState}</span>
                          <span
                            className={
                              version.ingestionStatus === "failed"
                                ? "badge warning"
                                : "badge"
                            }
                          >
                            {version.ingestionStatus}
                          </span>
                        </div>
                      </div>

                      <div className="meta">
                        <span>{version.sourceFilename}</span>
                        <span>{formatDate(version.updatedAt)}</span>
                      </div>

                      {version.publicationState !== "published" &&
                      version.ingestionStatus === "indexed" ? (
                        <form action={publishRunbookVersionAction}>
                          <input name="runbookId" type="hidden" value={runbook.id} />
                          <input name="versionId" type="hidden" value={version.id} />
                          <button type="submit">Publish this version</button>
                        </form>
                      ) : null}
                    </section>
                  ))}
              </div>
            </article>
          ))}
        </section>
      </section>
    </main>
  );
}
