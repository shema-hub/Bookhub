from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Book, Transaction
from .serializers import BookSerializer, TransactionSerializer
from users.models import User

class BookListCreateView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['title', 'author', 'isbn', 'copies_available']

class BookRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class CheckoutBookView(generics.CreateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        book_id = request.data.get('book')
        try:
            book = Book.objects.get(pk=book_id)
        except Book.DoesNotExist:
            return Response({'error': 'Book not found'}, status=status.HTTP_404_NOT_FOUND)

        if book.copies_available <= 0:
            return Response({'error': 'No copies available'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if user already has this book checked out
        existing_transaction = Transaction.objects.filter(
            user=request.user,
            book=book,
            is_returned=False
        ).exists()
        
        if existing_transaction:
            return Response({'error': 'You already have this book checked out'}, status=status.HTTP_400_BAD_REQUEST)

        # Create transaction
        transaction = Transaction.objects.create(
            user=request.user,
            book=book,
            is_returned=False
        )

        # Update book copies
        book.copies_available -= 1
        book.save()

        serializer = self.get_serializer(transaction)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class ReturnBookView(generics.UpdateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def update(self, request, *args, **kwargs):
        transaction = self.get_object()
        
        if transaction.user != request.user:
            return Response({'error': 'You cannot return a book you did not checkout'}, status=status.HTTP_403_FORBIDDEN)
        
        if transaction.is_returned:
            return Response({'error': 'This book has already been returned'}, status=status.HTTP_400_BAD_REQUEST)
        
        transaction.is_returned = True
        transaction.return_date = timezone.now()
        transaction.save()
        
        # Update book copies
        book = transaction.book
        book.copies_available += 1
        book.save()
        
        serializer = self.get_serializer(transaction)
        return Response(serializer.data)

class UserTransactionsView(generics.ListAPIView):
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)