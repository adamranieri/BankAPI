from flask import Flask

from daos.book_dao_postgres import BookDaoPostgres
from exceptions.book_unavailable_error import BookUnavailableError
from exceptions.not_found_exception import ResourceNotFoundError
from services.book_service_impl import BookServiceImpl

book_dao = BookDaoPostgres()
book_service = BookServiceImpl(book_dao)  # Dependency Injection

def add_book_routes(app: Flask):


    @app.route("/books/<book_id>", methods=["DELETE"])
    def delete_book(book_id: str):
        try:
            book_service.remove_book(int(book_id))
            return "Deleted successfully", 200
        except ResourceNotFoundError as e:
            return "The resource could not be found", 404

    @app.route("/books/<book_id>/checkout", methods=["PATCH"])
    def checkout_book(book_id: str):
        try:
            book_service.checkout_book(int(book_id))
            return f"The book with id {book_id} was successfully checked out"
        except BookUnavailableError as e:
            return str(e), 422  # request could not be processed even though all the information and formatting is correct
