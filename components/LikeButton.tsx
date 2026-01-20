import React from 'react';

interface LikeButtonProps {
  likes: number;
  liked: boolean;
  onToggle: () => void;
  disabled?: boolean;
  variant?: 'card' | 'modal';
}

export default function LikeButton({ likes, liked, onToggle, disabled, variant = 'card' }: LikeButtonProps) {
  const baseClasses =
    variant === 'card'
      ? 'absolute top-3 right-3 rounded-full bg-white/90 px-3 py-1 text-xs shadow-sm hover:bg-white'
      : 'flex items-center gap-3 rounded-full border border-gray-200 px-4 py-2 text-sm';

  const heartColor = liked ? 'text-rose-500' : 'text-gray-400';

  return (
    <button
      type="button"
      onClick={(event) => {
        event.stopPropagation();
        if (!disabled) {
          onToggle();
        }
      }}
      className={`${baseClasses} transition-colors ${disabled ? 'opacity-60 cursor-not-allowed' : ''}`}
      aria-pressed={liked}
      disabled={disabled}
    >
      <svg
        className={`w-4 h-4 ${heartColor}`}
        viewBox="0 0 24 24"
        fill={liked ? 'currentColor' : 'none'}
        stroke="currentColor"
        strokeWidth={1.8}
      >
        <path d="M12 21s-6.6-4.35-9-8.1C1.03 11.07 1 8.7 3 7c1.5-1.3 3.75-1.2 5.2.1L12 10l3.8-2.9c1.45-1.3 3.7-1.4 5.2-.1 2 1.7 1.97 4.07 0 5.9C18.6 16.65 12 21 12 21z" />
      </svg>
      {variant === 'modal' && (
        <span className="text-sm font-medium text-gray-700">
          {Intl.NumberFormat('en-US').format(Math.max(0, likes))}
        </span>
      )}
      {variant === 'card' && (
        <span className="ml-2 text-xs font-semibold text-gray-600">
          {Intl.NumberFormat('en-US', { notation: 'compact' }).format(Math.max(0, likes))}
        </span>
      )}
    </button>
  );
}
