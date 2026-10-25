import { useEffect, useState } from 'react';

// Membaca data dari localStorage dan menyimpannya setiap kali state berubah.
export default function useLocalStorage(key, initialValue) {
  const [value, setValue] = useState(() => {
    try {
      const saved = localStorage.getItem(key);
      return saved ? JSON.parse(saved) : initialValue;
    } catch {
      return initialValue;
    }
  });

  useEffect(() => {
    try {
      localStorage.setItem(key, JSON.stringify(value));
    } catch (error) {
      console.error('Gagal menyimpan data ke localStorage:', error);
    }
  }, [key, value]);

  return [value, setValue];
}