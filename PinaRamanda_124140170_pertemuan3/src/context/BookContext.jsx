import { createContext, useContext } from 'react';
import PropTypes from 'prop-types';
import useLocalStorage from '../hooks/useLocalStorage.js';

const BookContext = createContext(null);

export function BookProvider({ children }) {
  const [books, setBooks] = useLocalStorage('petalpages-books', []);

  const addBook = (book) => {
    setBooks((current) => [{ ...book, id: `${Date.now()}-${Math.random().toString(16).slice(2)}` }, ...current]);
  };

  const updateBook = (updatedBook) => {
    setBooks((current) => current.map((book) => book.id === updatedBook.id ? updatedBook : book));
  };

  const deleteBook = (id) => {
    setBooks((current) => current.filter((book) => book.id !== id));
  };

  return (
    <BookContext.Provider value={{ books, addBook, updateBook, deleteBook }}>
      {children}
    </BookContext.Provider>
  );
}
BookProvider.propTypes = { children: PropTypes.node.isRequired };

export function useBooks() {
  const context = useContext(BookContext);
  if (!context) throw new Error('useBooks harus digunakan di dalam BookProvider');
  return context;
}