"use client";

import type { ReactNode } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";

type WorkspaceShellProps = {
  children: ReactNode;
};

const NAV_ITEMS = [
  { href: "/runbooks", label: "Runbooks" },
  { href: "/agent", label: "Agent Chat" },
];

export function WorkspaceShell({ children }: WorkspaceShellProps) {
  const pathname = usePathname();

  return (
    <div className="workspace-shell">
      <header className="workspace-topbar">
        <div>
          <p className="brand-kicker">SRE agent</p>
          <Link className="brand-link" href="/runbooks">
            Runbook Manager
          </Link>
        </div>

        <nav className="workspace-nav" aria-label="Primary">
          {NAV_ITEMS.map((item) => {
            const isActive = pathname === item.href || pathname.startsWith(`${item.href}/`);
            return (
              <Link
                aria-current={isActive ? "page" : undefined}
                className={`workspace-nav__link${isActive ? " workspace-nav__link--active" : ""}`}
                href={item.href}
                key={item.href}
              >
                {item.label}
              </Link>
            );
          })}
        </nav>
      </header>

      <main className="workspace-content">{children}</main>
    </div>
  );
}
