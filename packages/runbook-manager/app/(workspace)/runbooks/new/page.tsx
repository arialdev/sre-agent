import { createRunbookAction } from "@/app/actions";

export default function NewRunbookPage() {
  return (
    <section className="page-section">
      <div className="page-header page-header--centered">
        <div className="page-header__content">
          <p className="eyebrow">Create runbook</p>
          <h1>Publish a new runbook from a markdown file.</h1>
          <p className="page-copy">
            A runbook consists of a title, one markdown file, and optional tags.
            Paste input and revision publishing are intentionally out of scope for now.
          </p>
        </div>
      </div>

      <section className="panel panel-form panel-form--single">
        <div className="panel-header">
          <div>
            <p className="eyebrow">New runbook</p>
            <h2>Upload markdown</h2>
          </div>
        </div>

        <form action={createRunbookAction} className="runbook-form">
          <label>
            Title
            <input name="title" placeholder="Redis cache eviction" required />
          </label>
          <label>
            Tags
            <input
              name="tags"
              placeholder="redis, cache, eviction"
            />
          </label>
          <label>
            Markdown file
            <input name="file" type="file" accept=".md,text/markdown" required />
          </label>
          <button type="submit">Create runbook</button>
        </form>
      </section>
    </section>
  );
}
