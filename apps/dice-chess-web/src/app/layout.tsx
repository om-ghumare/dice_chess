import type { Metadata } from "next";
import { Inter, Outfit } from "next/font/google";
import "./globals.css";

const inter = Inter({
  variable: "--font-body",
  subsets: ["latin"],
  display: "swap",
});

const outfit = Outfit({
  variable: "--font-heading",
  subsets: ["latin"],
  display: "swap",
});

export const metadata: Metadata = {
  title: "Dice Chess — Roll to Move",
  description: "A unique twist on chess where a dice roll determines which piece you can move. Play locally, vs AI, or online with friends!",
  keywords: ["chess", "dice chess", "board game", "multiplayer", "strategy"],
  openGraph: {
    title: "Dice Chess — Roll to Move",
    description: "A unique chess variant with a dice twist. Roll and strategize!",
    type: "website",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={`${inter.variable} ${outfit.variable}`}>
        {children}
      </body>
    </html>
  );
}
