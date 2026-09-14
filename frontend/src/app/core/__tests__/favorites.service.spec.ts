import { FavoritesService } from '../favorites.service';

describe('FavoritesService', () => {
  beforeEach(() => localStorage.clear());

  it('starts empty', () => {
    const service = new FavoritesService();
    expect(service.count()).toBe(0);
    expect(service.all()).toEqual([]);
  });

  it('toggles a property and persists it', () => {
    const service = new FavoritesService();

    expect(service.toggle('apartment-1')).toBe(true);
    expect(service.has('apartment-1')).toBe(true);
    expect(service.count()).toBe(1);

    const restored = new FavoritesService();
    expect(restored.has('apartment-1')).toBe(true);

    expect(restored.toggle('apartment-1')).toBe(false);
    expect(restored.count()).toBe(0);
  });

  it('recovers from invalid stored data', () => {
    localStorage.setItem('amalkpro.favorite-slugs', 'not-json');
    const service = new FavoritesService();
    expect(service.all()).toEqual([]);
  });
});
