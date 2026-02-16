-- Create code_matches table for sharing Code Match results
CREATE TABLE IF NOT EXISTS code_matches (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  hash text UNIQUE NOT NULL,
  code text NOT NULL,
  metrics jsonb NOT NULL,
  results jsonb NOT NULL,
  views integer DEFAULT 0,
  created_at timestamp with time zone DEFAULT now(),
  updated_at timestamp with time zone DEFAULT now()
);

-- Create index on hash for fast lookups
CREATE INDEX IF NOT EXISTS idx_code_matches_hash ON code_matches(hash);

-- Create index on created_at for trending/recent queries
CREATE INDEX IF NOT EXISTS idx_code_matches_created_at ON code_matches(created_at DESC);

-- Enable Row Level Security
ALTER TABLE code_matches ENABLE ROW LEVEL SECURITY;

-- Allow everyone to read code matches (public sharing)
CREATE POLICY "Public read access for code_matches"
ON code_matches FOR SELECT
TO public
USING (true);

-- Allow anyone to insert code matches
CREATE POLICY "Public insert access for code_matches"
ON code_matches FOR INSERT
TO public
WITH CHECK (true);

-- Allow updates for view count
CREATE POLICY "Public update views for code_matches"
ON code_matches FOR UPDATE
TO public
USING (true)
WITH CHECK (true);

-- Function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_code_matches_updated_at()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = now();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger to automatically update updated_at
CREATE TRIGGER update_code_matches_updated_at
BEFORE UPDATE ON code_matches
FOR EACH ROW
EXECUTE FUNCTION update_code_matches_updated_at();

-- Comments
COMMENT ON TABLE code_matches IS 'Stores Code Match search results for sharing and analytics';
COMMENT ON COLUMN code_matches.hash IS 'Unique short hash for URL sharing (e.g., abc123)';
COMMENT ON COLUMN code_matches.code IS 'Original code snippet submitted by user';
COMMENT ON COLUMN code_matches.metrics IS 'DesignMetrics object as JSON';
COMMENT ON COLUMN code_matches.results IS 'Array of matched designs with scores as JSON';
COMMENT ON COLUMN code_matches.views IS 'Number of times this match has been viewed';
