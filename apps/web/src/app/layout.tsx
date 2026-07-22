import React from 'react';
import type { Metadata } from "next";
import Providers from "./providers";
import "./global.css";

export const metadata: Metadata = {
  title: "VedAI - Ancient Wisdom. Powered by AI.",
  description: "Enterprise Vedic Astrology platform mapping astronomical charts, traditional readings, and AI synthesis.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <head>
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
        <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&display=swap" rel="stylesheet" />
      </head>
      <body className="antialiased min-h-screen text-slate-100 bg-[#030712] selection:bg-indigo-500/30 selection:text-white" style={{ fontFamily: "'Outfit', sans-serif" }}>
        <Providers>
          {children}
        </Providers>
      </body>
    </html>
  );
}
