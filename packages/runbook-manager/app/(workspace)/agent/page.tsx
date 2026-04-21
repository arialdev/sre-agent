export default function AgentChatPage() {
  return (
    <section className="page-section">
      <div className="page-header">
        <div>
          <p className="eyebrow">Agent chat</p>
          <h1>Chat with the agent</h1>
        </div>
        <p className="page-copy">
          This area is reserved for the guided incident chat workflow that will
          connect directly to the SRE agent.
        </p>
      </div>

      <article className="placeholder-card">
        <span className="status-pill">Future surface</span>
        <h2>coming soon</h2>
        <p>
          The runbook workspace is ready now. The agent conversation experience
          will land in this dedicated area in a later change.
        </p>
      </article>
    </section>
  );
}
