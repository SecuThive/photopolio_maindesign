const parsePlacementIds = (value?: string | null) => {
  if (!value) {
    return [] as number[];
  }

  return value
    .split(',')
    .map((segment) => Number.parseInt(segment.trim(), 10))
    .filter((id) => Number.isFinite(id));
};

export const getPlacementIds = (envKey?: string) => {
  if (envKey) {
    const scopedValue = process.env[envKey];
    if (scopedValue) {
      return parsePlacementIds(scopedValue);
    }
  }

  return parsePlacementIds(process.env.NEXT_PUBLIC_EZOIC_PLACEMENTS);
};
