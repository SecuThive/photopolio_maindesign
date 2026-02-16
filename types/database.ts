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
  tags?: string[] | null;
  status: 'published' | 'archived';
  strategy_notes?: string | null;
  psychology_notes?: string | null;
  usage_notes?: string | null;
  performance_notes?: string | null;
  accessibility_notes?: string | null;
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

export type WebVitalsEvent = {
  id: string;
  created_at: string;
  metric: string;
  rating: string | null;
  value: number;
  delta: number | null;
  label: string | null;
  page: string | null;
  session_id: string | null;
  navigation_type: string | null;
  blocked_third_party: boolean | null;
  connection: string | null;
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

export type BlogPost = {
  id: string;
  slug: string;
  title: string;
  excerpt: string | null;
  content: string;
  category: string | null;
  author: string | null;
  author_role: string | null;
  author_avatar_url: string | null;
  cover_image_url: string | null;
  tags: string[] | null;
  published_at: string | null;
  status: 'draft' | 'published';
  created_at: string;
  updated_at: string;
};

export type CodeMatch = {
  id: string;
  hash: string;
  code: string;
  metrics: any; // DesignMetrics as JSON
  results: any; // Array of matched designs as JSON
  views: number;
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
          tags?: string[] | null;
          status?: 'published' | 'archived';
          strategy_notes?: string | null;
          psychology_notes?: string | null;
          usage_notes?: string | null;
          performance_notes?: string | null;
          accessibility_notes?: string | null;
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
          tags?: string[] | null;
          status?: 'published' | 'archived';
          strategy_notes?: string | null;
          psychology_notes?: string | null;
          usage_notes?: string | null;
          performance_notes?: string | null;
          accessibility_notes?: string | null;
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
      web_vitals_events: {
        Row: WebVitalsEvent;
        Insert: {
          id?: string;
          created_at?: string;
          metric: string;
          rating?: string | null;
          value: number;
          delta?: number | null;
          label?: string | null;
          page?: string | null;
          session_id?: string | null;
          navigation_type?: string | null;
          blocked_third_party?: boolean | null;
          connection?: string | null;
          user_agent?: string | null;
        };
        Update: {
          id?: string;
          created_at?: string;
          metric?: string;
          rating?: string | null;
          value?: number;
          delta?: number | null;
          label?: string | null;
          page?: string | null;
          session_id?: string | null;
          navigation_type?: string | null;
          blocked_third_party?: boolean | null;
          connection?: string | null;
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
      posts: {
        Row: BlogPost;
        Insert: {
          id?: string;
          slug: string;
          title: string;
          excerpt?: string | null;
          content: string;
          category?: string | null;
          author?: string | null;
          author_role?: string | null;
          author_avatar_url?: string | null;
          cover_image_url?: string | null;
          tags?: string[] | null;
          published_at?: string | null;
          status?: 'draft' | 'published';
          created_at?: string;
          updated_at?: string;
        };
        Update: {
          id?: string;
          slug?: string;
          title?: string;
          excerpt?: string | null;
          content?: string;
          category?: string | null;
          author?: string | null;
          author_role?: string | null;
          author_avatar_url?: string | null;
          cover_image_url?: string | null;
          tags?: string[] | null;
          published_at?: string | null;
          status?: 'draft' | 'published';
          created_at?: string;
          updated_at?: string;
        };
      };
      code_matches: {
        Row: CodeMatch;
        Insert: {
          id?: string;
          hash: string;
          code: string;
          metrics: any;
          results: any;
          views?: number;
          created_at?: string;
          updated_at?: string;
        };
        Update: {
          id?: string;
          hash?: string;
          code?: string;
          metrics?: any;
          results?: any;
          views?: number;
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
