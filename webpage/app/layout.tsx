import type { Metadata } from "next";
import { IBM_Plex_Mono, IBM_Plex_Sans, Source_Serif_4 } from "next/font/google";
import "./globals.css";

const serif = Source_Serif_4({
  subsets: ["latin"],
  variable: "--font-serif",
  weight: ["400", "600", "700"],
});
const sans = IBM_Plex_Sans({
  subsets: ["latin"],
  variable: "--font-sans",
  weight: ["400", "500", "600"],
});
const mono = IBM_Plex_Mono({
  subsets: ["latin"],
  variable: "--font-mono",
  weight: ["400", "500"],
});

export const metadata: Metadata = {
  metadataBase: new URL("https://openniw.com"),
  title: "OpenNIW — organize your NIW · EB-1A · O-1 · I-485 with your own AI",
  description:
    "Free, open-source skills that help you organize and speed up your own "
    + "EB-2 NIW or EB-1A self-petition, O-1A petition kit, or employment-based "
    + "I-485, using the coding "
    + "agent you already have. Free statistical evaluation against 10,999 approved "
    + "cases. No accounts, no fees. Not a law firm; not legal advice.",
  openGraph: {
    title: "OpenNIW — organize your NIW · EB-1A · O-1 · I-485 with your own AI",
    description:
      "Free, open-source NIW / EB-1A / O-1 / I-485 paperwork tooling driven by your own "
      + "AI subscription. Free statistical evaluation against 10,999 approved cases. Not a "
      + "law firm; not legal advice.",
    url: "https://openniw.com",
    siteName: "OpenNIW",
  },
};

export default function RootLayout({
  children,
}: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en">
      <body
        className={`${serif.variable} ${sans.variable} ${mono.variable} antialiased min-h-screen`}
        style={{ fontFamily: "var(--font-sans), system-ui, sans-serif" }}
      >
        {children}
      </body>
    </html>
  );
}
