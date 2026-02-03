-- Create newsletter_subscribers table
CREATE TABLE IF NOT EXISTS public.newsletter_subscribers (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  email VARCHAR(255) UNIQUE NOT NULL,
  subscribed_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  is_active BOOLEAN DEFAULT TRUE,
  ip_address VARCHAR(45),
  user_agent TEXT,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create index on email for faster lookups
CREATE INDEX IF NOT EXISTS idx_newsletter_subscribers_email ON public.newsletter_subscribers(email);

-- Create index on subscribed_at for sorting
CREATE INDEX IF NOT EXISTS idx_newsletter_subscribers_subscribed_at ON public.newsletter_subscribers(subscribed_at DESC);

-- Enable Row Level Security
ALTER TABLE public.newsletter_subscribers ENABLE ROW LEVEL SECURITY;

-- Drop existing policies if they exist
DROP POLICY IF EXISTS "Allow anyone to subscribe" ON public.newsletter_subscribers;
DROP POLICY IF EXISTS "Allow authenticated users to read subscribers" ON public.newsletter_subscribers;
DROP POLICY IF EXISTS "Allow authenticated users to update subscribers" ON public.newsletter_subscribers;

-- Create policy to allow anyone to insert (subscribe)
CREATE POLICY "Allow anyone to subscribe" ON public.newsletter_subscribers
  FOR INSERT
  TO anon, authenticated
  WITH CHECK (true);

-- Create policy to allow only authenticated users to read
CREATE POLICY "Allow authenticated users to read subscribers" ON public.newsletter_subscribers
  FOR SELECT
  TO authenticated
  USING (true);

-- Create policy to allow only authenticated users to update
CREATE POLICY "Allow authenticated users to update subscribers" ON public.newsletter_subscribers
  FOR UPDATE
  TO authenticated
  USING (true);

-- Add trigger to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_newsletter_subscribers_updated_at()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Drop existing trigger if it exists
DROP TRIGGER IF EXISTS newsletter_subscribers_updated_at ON public.newsletter_subscribers;

CREATE TRIGGER newsletter_subscribers_updated_at
  BEFORE UPDATE ON public.newsletter_subscribers
  FOR EACH ROW
  EXECUTE FUNCTION update_newsletter_subscribers_updated_at();

-- Add comment to table
COMMENT ON TABLE public.newsletter_subscribers IS 'Stores newsletter subscriber email addresses and subscription metadata';
