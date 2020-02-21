import argparse
from statistics import mean

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('input_path', type=str,
                        help='Path for the input file.')
    args = parser.parse_args()
    

    with open(args.input_path, 'r') as input_file:
        string = input_file.read()
        lines = string.split('\n')
        total_books, total_libraries, total_days = [int(str_) for str_ in lines[0].split(' ')]

        book_scores = {id_: int(str_) for id_, str_ in enumerate(lines[1].split(' '))}
        
        libraries = {}
        library_id = 0
        for i in range(2, 2+total_libraries+1, 2):
            library_info = lines[i].split(' ')
            libraries.update({library_id: {'total_books': int(library_info[0]), 'signup_time': int(library_info[1]), 'ships_per_day': int(library_info[2]), 'selected': False}})
            library_books_info = lines[i+1].split(' ')
            libraries.get(library_id).update({'books': {int(book) for book in library_books_info}})
            library_id +=1

        inverted_index = {i: {x for x in libraries if i in libraries.get(x).get('books')} for i in range(total_books)}

        scanned_books = set()
        shipped_books = {library: [] for library in libraries}
        selected_libraries = []
        potential_books = set()
        signing_up = False
        for day in range(total_days):
            avg_freq_book = {key: len(value)/total_libraries for key, value in inverted_index.items()}
            avg_freq_library = {library: mean([avg_freq_book.get(book) for book in libraries.get(library).get('books')]) for library in libraries if not libraries.get(library).get('selected')}

            library_scores = {library: (sum([book_scores.get(book_id) for book_id in libraries.get(library).get('books')]) * libraries.get(library).get('ships_per_day')) \
                                    /(libraries.get(library).get('signup_time') * avg_freq_library.get(library)) 
                      for library in libraries if not libraries.get(library).get('selected') and (libraries.get(library).get('signup_time') + day < total_days)}

            if library_scores:
                max_score_library = max(library_scores, key=library_scores.get)
                if not signing_up:
                    libraries[max_score_library]['selected'] = True
                selected_libraries.append(max_score_library)

            for library in libraries:
                if libraries[library]['selected']:
                    if libraries[library]['signup_time'] > 0:
                        libraries[library]['signup_time'] -= 1
                    else:
                        signing_up = False

                    if (not libraries[library]['signup_time']) and libraries[library]['books']:
                        ships = libraries[library]['ships_per_day']
                        potential_books = [book for book in libraries[library]['books'] if book not in scanned_books]
                        while ships and libraries[library]['books']:
                            if potential_books:
                                max_score_book = max(potential_books, key=book_scores.get)
                                scanned_books.add(max_score_book)
                                shipped_books[library].append(max_score_book)
                                potential_books.remove(max_score_book)
                            else:
                                max_score_book = max(libraries[library]['books'], key=book_scores.get)
                                shipped_books[library].append(max_score_book)
                            libraries[library]['books'].remove(max_score_book)
                            ships -= 1

    with open(args.input_path.split(".")[0]+".out", "w") as output_file:
        output_file.write(f'{len(selected_libraries)}\n')
        for library in selected_libraries:
            output_file.write(f'{library} {len(shipped_books[library])}\n')
            output_file.write(f"{' '.join([str(book) for book in shipped_books[library]])}\n")