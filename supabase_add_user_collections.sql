-- User Collections: Allow users to organize saved designs into collections with notes and sharing

-- User collections table (collection metadata)
CREATE TABLE IF NOT EXISTS user_collections (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  share_hash text UNIQUE NOT NULL, -- Short hash for public sharing (e.g., 8 chars)
  name text NOT NULL,
  description text,
  is_public boolean DEFAULT false, -- Whether this collection is publicly shareable
  created_at timestamp with time zone DEFAULT now(),
  updated_at timestamp with time zone DEFAULT now()
);

-- Collection items table (designs in each collection with notes)
CREATE TABLE IF NOT EXISTS user_collection_items (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  collection_id uuid NOT NULL REFERENCES user_collections(id) ON DELETE CASCADE,
  design_id uuid NOT NULL,
  note text, -- User's personal note about this design in the collection
  sort_order integer DEFAULT 0, -- For custom ordering within collection
  created_at timestamp with time zone DEFAULT now(),
  updated_at timestamp with time zone DEFAULT now(),
  UNIQUE(collection_id, design_id) -- Prevent duplicate designs in same collection
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_user_collections_share_hash ON user_collections(share_hash);
CREATE INDEX IF NOT EXISTS idx_user_collection_items_collection_id ON user_collection_items(collection_id);
CREATE INDEX IF NOT EXISTS idx_user_collection_items_design_id ON user_collection_items(design_id);

-- Enable Row Level Security
ALTER TABLE user_collections ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_collection_items ENABLE ROW LEVEL SECURITY;

-- Public read access for public collections (via share link)
CREATE POLICY "Public read access for public collections"
ON user_collections FOR SELECT
TO public
USING (is_public = true);

CREATE POLICY "Public read access for public collection items"
ON user_collection_items FOR SELECT
TO public
USING (
  EXISTS (
    SELECT 1 FROM user_collections
    WHERE user_collections.id = user_collection_items.collection_id
    AND user_collections.is_public = true
  )
);

-- Allow anyone to create collections (anonymous collections stored by share_hash)
CREATE POLICY "Public insert access for collections"
ON user_collections FOR INSERT
TO public
WITH CHECK (true);

CREATE POLICY "Public insert access for collection items"
ON user_collection_items FOR INSERT
TO public
WITH CHECK (true);

-- Allow anyone to update their own collections (matched by share_hash in app logic)
CREATE POLICY "Public update access for collections"
ON user_collections FOR UPDATE
TO public
USING (true)
WITH CHECK (true);

CREATE POLICY "Public update access for collection items"
ON user_collection_items FOR UPDATE
TO public
USING (true)
WITH CHECK (true);

-- Allow anyone to delete their own collections
CREATE POLICY "Public delete access for collections"
ON user_collections FOR DELETE
TO public
USING (true);

CREATE POLICY "Public delete access for collection items"
ON user_collection_items FOR DELETE
TO public
USING (true);

-- Function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_user_collections_updated_at()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = now();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION update_user_collection_items_updated_at()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = now();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Triggers to automatically update updated_at
CREATE TRIGGER update_user_collections_updated_at
BEFORE UPDATE ON user_collections
FOR EACH ROW
EXECUTE FUNCTION update_user_collections_updated_at();

CREATE TRIGGER update_user_collection_items_updated_at
BEFORE UPDATE ON user_collection_items
FOR EACH ROW
EXECUTE FUNCTION update_user_collection_items_updated_at();

-- Helper function to generate short share hash
CREATE OR REPLACE FUNCTION generate_share_hash()
RETURNS text AS $$
DECLARE
  chars text := 'abcdefghijklmnopqrstuvwxyz0123456789';
  result text := '';
  i integer;
BEGIN
  FOR i IN 1..8 LOOP
    result := result || substr(chars, floor(random() * length(chars) + 1)::integer, 1);
  END LOOP;
  RETURN result;
END;
$$ LANGUAGE plpgsql;

-- Comments
COMMENT ON TABLE user_collections IS 'User-created collections for organizing saved designs';
COMMENT ON COLUMN user_collections.share_hash IS 'Unique 8-character hash for sharing collection publicly (e.g., /saved/abc12345)';
COMMENT ON COLUMN user_collections.is_public IS 'Whether collection is accessible via share link';
COMMENT ON TABLE user_collection_items IS 'Designs saved within each collection with optional notes';
COMMENT ON COLUMN user_collection_items.note IS 'User note about why this design was saved or how to use it';
COMMENT ON COLUMN user_collection_items.sort_order IS 'Custom ordering within collection (lower numbers first)';
