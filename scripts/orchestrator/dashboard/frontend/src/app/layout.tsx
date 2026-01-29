// Autopilot Dashboard Layout
// Copyright (c) 2026 Jeremy McSpadden <jeremy@fluxlabs.net>

import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'Autopilot Dashboard',
  description: 'Manage autonomous coding projects',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="min-h-screen bg-gray-950 text-gray-100">
        {children}
      </body>
    </html>
  );
}
