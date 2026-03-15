import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "SkinSense AI",
  description: "AI-powered skin analysis and personalized skincare recommendations",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
