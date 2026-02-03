export type Design = {
  id: string;
  title: string;
  description: string | null;
  image_url: string;
  category: string | null;
  prompt: string | null;
  code: string | null;
  created_at: string;
  updated_at: string;
  likes: number | null;
  views?: number | null;
  slug?: string | null;
  colors?: string[] | null;
  status: 'published' | 'archived';
  colorable_regions?: Array<{
    id: string;
    name: string;
    type: string;
    x: number;
    y: number;
    width: number;
    height: number;
  }> | null;
};

export type DesignWithSlug = Design & { slug: string };

export type PageView = {
  id: string;
  created_at: string;
  page: string | null;
  referer: string | null;
  user_agent: string | null;
};

export type NewsletterSubscriber = {
  id: string;
  email: string;
  subscribed_at: string;
  is_active: boolean;
  ip_address: string | null;
  user_agent: string | null;
  created_at: string;
  updated_at: string;
};

export type Database = {
  public: {
    Tables: {
      designs: {
        Row: Design;
        Insert: {
          id?: string;
          title: string;
          description?: string | null;
          image_url: string;
          category?: string | null;
          prompt?: string | null;
          code?: string | null;
          created_at?: string;
          updated_at?: string;
          likes?: number | null;
          views?: number | null;
          colors?: string[] | null;
          status?: 'published' | 'archived';
        };
        Update: {
          id?: string;
          title?: string;
          description?: string | null;
          image_url?: string;
          category?: string | null;
          prompt?: string | null;
          code?: string | null;
          created_at?: string;
          updated_at?: string;
          likes?: number | null;
          views?: number | null;
          colors?: string[] | null;
          status?: 'published' | 'archived';
        };
      };
      design_likes: {
        Row: {
          id: string;
          created_at: string;
          design_id: string;
          token: string;
        };
        Insert: {
          id?: string;
          created_at?: string;
          design_id: string;
          token: string;
        };
        Update: {
          id?: string;
          created_at?: string;
          design_id?: string;
          token?: string;
        };
      };
      page_views: {
        Row: PageView;
        Insert: {
          id?: string;
          created_at?: string;
          page?: string | null;
          referer?: string | null;
          user_agent?: string | null;
        };
        Update: {
          id?: string;
          created_at?: string;
          page?: string | null;
          referer?: string | null;
          user_agent?: string | null;
        };
      };
      newsletter_subscribers: {
        Row: NewsletterSubscriber;
        Insert: {
          id?: string;
          email: string;
          subscribed_at?: string;
          is_active?: boolean;
          ip_address?: string | null;
          user_agent?: string | null;
          created_at?: string;
          updated_at?: string;
        };
        Update: {
          id?: string;
          email?: string;
          subscribed_at?: string;
          is_active?: boolean;
          ip_address?: string | null;
          user_agent?: string | null;
          created_at?: string;
          updated_at?: string;
        };
      };
    };
    Views: {
      [_ in never]: never;
    };
    Functions: {
      [_ in never]: never;
    };
    Enums: {
      [_ in never]: never;
    };
  };
};
