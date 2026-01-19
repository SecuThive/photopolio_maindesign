"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { Command } from "cmdk";
import { createPortal } from "react-dom";

const navigationItems = [
  { label: "Home", href: "/", description: "Return to the gallery home" },
  { label: "About", href: "/about", description: "Learn more about Base Syntax" },
  { label: "Contact", href: "/contact", description: "Get in touch with the team" },
  { label: "Privacy Policy", href: "/privacy-policy", description: "Review data practices" },
];

const categoryItems = [
  { label: "All Designs", value: null, href: "/" },
  { label: "Landing Page", value: "Landing Page", href: "/?category=Landing%20Page" },
  { label: "Dashboard", value: "Dashboard", href: "/?category=Dashboard" },
  { label: "E-commerce", value: "E-commerce", href: "/?category=E-commerce" },
  { label: "Portfolio", value: "Portfolio", href: "/?category=Portfolio" },
  { label: "Blog", value: "Blog", href: "/?category=Blog" },
  { label: "Components", value: "Components", href: "/?category=Components" },
];

export default function CommandPalette() {
  const router = useRouter();
  const [open, setOpen] = useState(false);
  const [mounted, setMounted] = useState(false);
  const [searchValue, setSearchValue] = useState("");

  useEffect(() => {
    setMounted(true);
  }, []);

  useEffect(() => {
    const handleKey = (event: KeyboardEvent) => {
      const isKShortcut = event.key.toLowerCase() === "k" && (event.metaKey || event.ctrlKey);
      if (isKShortcut) {
        event.preventDefault();
        setOpen((prev) => !prev);
        return;
      }

      if (event.key === "Escape") {
        setOpen(false);
      }
    };

    window.addEventListener("keydown", handleKey);
    return () => window.removeEventListener("keydown", handleKey);
  }, []);

  useEffect(() => {
    const handleOpenEvent = () => setOpen(true);
    window.addEventListener("open-command-palette", handleOpenEvent);
    return () => window.removeEventListener("open-command-palette", handleOpenEvent);
  }, []);

  useEffect(() => {
    if (!open) {
      setSearchValue("");
    }
  }, [open]);

  const handleNavigate = (href: string) => {
    setOpen(false);
    router.push(href);
  };

  if (!mounted) {
    return null;
  }

  return createPortal(
    <div
      className={`fixed inset-0 z-[9999] transition-opacity duration-150 ${
        open ? "pointer-events-auto opacity-100" : "pointer-events-none opacity-0"
      }`}
      role="dialog"
      aria-modal="true"
      aria-label="Command palette"
    >
      <div
        className="absolute inset-0 bg-black/50"
        onClick={() => setOpen(false)}
        aria-hidden="true"
      />

      <div className="relative mx-auto mt-24 w-full max-w-2xl px-4">
        <Command className="w-full overflow-hidden rounded-2xl border border-gray-200 bg-white text-gray-900 shadow-2xl">
          <div className="flex items-center border-b border-gray-100 px-4">
            <Command.Input
              autoFocus={open}
              value={searchValue}
              onValueChange={setSearchValue}
              placeholder="빠르게 이동하거나 카테고리를 검색하세요..."
              placeholder="Jump to a page or search categories..."
              className="h-14 w-full bg-transparent text-base outline-none placeholder:text-gray-400"
            />
            <kbd className="ml-3 hidden rounded-md border border-gray-200 px-2 py-1 text-xs uppercase text-gray-400 sm:block">
              ⌘K
            </kbd>
          </div>

          <Command.List className="max-h-[420px] overflow-y-auto">
            <Command.Empty className="px-4 py-6 text-center text-sm text-gray-400">
              No matches found.
            </Command.Empty>

            <Command.Group heading="Navigation" className="px-2 py-3 text-xs uppercase tracking-wider text-gray-400">
              {navigationItems.map((item) => (
                <Command.Item
                  key={item.href}
                  value={item.label}
                  onSelect={() => handleNavigate(item.href)}
                  className="flex flex-col rounded-lg px-3 py-3 text-sm text-gray-800 data-[selected=true]:bg-gray-100"
                >
                  <span className="font-medium text-gray-900">{item.label}</span>
                  <span className="text-xs text-gray-500">{item.description}</span>
                </Command.Item>
              ))}
            </Command.Group>

            <Command.Separator className="mx-3 my-2 h-px bg-gray-100" />

            <Command.Group heading="Categories" className="px-2 py-3 text-xs uppercase tracking-wider text-gray-400">
              {categoryItems.map((category) => (
                <Command.Item
                  key={category.label}
                  value={category.label}
                  onSelect={() => handleNavigate(category.href)}
                  className="flex items-center justify-between rounded-lg px-3 py-2 text-sm text-gray-800 data-[selected=true]:bg-gray-100"
                >
                  <span>{category.label}</span>
                  <span className="text-[10px] uppercase tracking-widest text-gray-400">Category</span>
                </Command.Item>
              ))}
            </Command.Group>
          </Command.List>

          <div className="border-t border-gray-100 px-4 py-3 text-right text-xs text-gray-400">
            Press Esc to close
          </div>
        </Command>
      </div>
    </div>,
    document.body
  );
}
