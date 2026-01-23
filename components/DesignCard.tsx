import React from 'react';
import Image from 'next/image';
import Link from 'next/link';
import { DesignWithSlug } from '@/types/database';
import LikeButton from './LikeButton';

interface DesignCardProps {
  design: DesignWithSlug;
  onClick: (e: React.MouseEvent<HTMLAnchorElement>) => void;
  likes: number;
  liked: boolean;
  onToggleLike: () => void;
  likeDisabled?: boolean;
  category?: string | null;
}

export default function DesignCard({ design, onClick, likes, liked, onToggleLike, likeDisabled, category }: DesignCardProps) {
  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
    });
  };

  const href = `/design/${design.slug}`;

  return (
    <Link
      href={href}
      onClick={onClick}
      className="block group cursor-pointer bg-white overflow-hidden transition-all duration-500 hover:luxury-shadow-lg"
    >
      <div className="relative aspect-[3/4] overflow-hidden bg-gray-100">
        <Image
          src={design.image_url}
          alt={design.title}
          fill
          className="object-cover object-top group-hover:scale-105 transition-transform duration-700 ease-out"
          sizes="(max-width: 640px) 100vw, (max-width: 1024px) 50vw, 25vw"
        />
        <div className="absolute inset-0 bg-black opacity-0 group-hover:opacity-10 transition-opacity duration-500"></div>
        <LikeButton likes={likes} liked={liked} onToggle={onToggleLike} disabled={likeDisabled} />
      </div>
      
      <div className="p-6 border-t border-gray-100">
        <h3 className="font-display text-xl text-black line-clamp-1 mb-2 tracking-tight">
          {design.title}
        </h3>
        
        {design.description && (
          <p className="text-sm text-gray-500 line-clamp-2 mb-3 font-light leading-relaxed">
            {design.description}
          </p>
        )}
        
        <div className="flex items-center justify-between text-xs text-gray-400 font-light tracking-wide">
          <span>{formatDate(design.created_at)}</span>
          {design.category && (
            <span className="px-3 py-1 bg-black text-white text-[10px] uppercase tracking-widest">
              {design.category}
            </span>
          )}
        </div>
      </div>
    </Link>
  );
}
