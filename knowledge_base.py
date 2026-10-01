import chromadb
from chromadb.api.types import Metadata

# Create a persistent ChromaDB client (data survives restarts)
client = chromadb.PersistentClient(path="./chroma")

# Create a collection called "my_knowledge"
collection = client.get_or_create_collection(
    name="my_knowledge",
    metadata={"description": "AI Engineering Foundations course content"},
)

print(f"Collection '{collection.name}' ready.")
print(f"Current document count: {collection.count()}")

# Add at least 15 documents covering content from at least 3 different modules you’ve completed.
documents = [
    "A relational database stores information in tables made up of rows and columns. Each table represents an entity, such as customers or orders, and each row represents one record.",
    "A primary key uniquely identifies each row in a database table. Primary keys help prevent duplicate records and let other tables refer to a specific record reliably.",
    "A foreign key links a record in one table to a record in another table. This relationship helps maintain referential integrity, such as ensuring every order belongs to an existing customer.",
    "SQL is the standard language used to define, query, and modify relational data. Commands such as SELECT, INSERT, UPDATE, and DELETE cover common data operations.",
    "The SELECT statement retrieves data from one or more tables. WHERE filters the rows returned, while ORDER BY sorts the results by one or more columns.",
    "SQL joins combine related rows from multiple tables using matching columns. An INNER JOIN returns matching rows, while a LEFT JOIN also keeps every row from the left table.",
    "Database normalization organizes data to reduce unnecessary duplication and update errors. Splitting related facts into linked tables can make data more consistent and easier to maintain.",
    "An index is a database structure that can speed up searches and joins on selected columns. Indexes use extra storage and can make writes slower, so they should be chosen for common query patterns.",
    "A REST API exposes resources through predictable URLs and standard HTTP methods. Clients use methods such as GET, POST, PUT, PATCH, and DELETE to read or change resource state.",
    "HTTP status codes communicate the outcome of an API request. For example, 200 indicates success, 201 indicates a resource was created, and 404 means the requested resource was not found.",
    "JSON is a common format for exchanging structured data between REST API clients and servers. Objects and arrays allow responses to represent records and collections in a readable way.",
    "HTTP headers carry information about a request or response, such as the content type or authorization credentials. The Content-Type header tells the server how to interpret a request body.",
    "API endpoints should validate incoming parameters and request bodies before processing them. Clear validation errors help clients correct malformed or incomplete requests.",
    "Pagination divides a large API result set into smaller portions. Page numbers, offsets, or cursors let clients retrieve results without transferring an entire collection at once.",
    "FastAPI uses Python type hints to define request data and validate it automatically. Typed models also help generate clear API documentation.",
    "Pydantic models describe the structure and constraints of data accepted or returned by a FastAPI application. FastAPI can use these models to parse request bodies and serialize responses.",
    "Path parameters identify a resource within an endpoint URL, while query parameters often control filtering or pagination. FastAPI lets developers declare both directly in route function signatures.",
    "FastAPI can generate interactive API documentation from route definitions and data models. The OpenAPI schema supports tools such as Swagger UI for trying endpoints in a browser.",
    "Streamlit turns Python scripts into interactive web applications with widgets such as buttons, sliders, and text inputs. A widget interaction reruns the script so the displayed output reflects the latest input.",
    "Streamlit's session state preserves values across script reruns for a user's session. It is useful for retaining selections, counters, or intermediate results as users interact with an app.",
]

# Unique ID assignment
ids = [f"doc_{i}" for i in range(len(documents))]

# Metadata with at least: module (which module it’s from) and topic (general category like "api", "database", "frontend", "ai")
metadatas: list[Metadata] = [
    {"module": "3", "topic": "relational-databases"},
    {"module": "3", "topic": "primary-keys"},
    {"module": "3", "topic": "foreign-keys"},
    {"module": "3", "topic": "sql-basics"},
    {"module": "3", "topic": "sql-queries"},
    {"module": "3", "topic": "sql-joins"},
    {"module": "3", "topic": "normalization"},
    {"module": "3", "topic": "database-indexes"},
    {"module": "4", "topic": "rest-fundamentals"},
    {"module": "4", "topic": "http-status-codes"},
    {"module": "4", "topic": "json"},
    {"module": "4", "topic": "http-headers"},
    {"module": "4", "topic": "api-validation"},
    {"module": "4", "topic": "pagination"},
    {"module": "5", "topic": "fastapi-type-hints"},
    {"module": "5", "topic": "pydantic-models"},
    {"module": "5", "topic": "fastapi-parameters"},
    {"module": "5", "topic": "openapi-docs"},
    {"module": "6", "topic": "streamlit-widgets"},
    {"module": "6", "topic": "streamlit-session-state"},
]

# Use collection.upsert() instead of collection.add() to handle re-runs without ID conflicts
collection.upsert(ids=ids, documents=documents, metadatas=metadatas)

print(f"Added {len(documents)} documents.")
print(f"Collection now has {collection.count()} documents.")

# Create loop to search the database until user types quit.
while True:
    search_text = input(
        "Search the database by typing a prompt here or type quit to exit: "
    )

    if search_text.strip().lower() == "quit":
        break

    while True:
        # Optional filtering (all searches all documents)
        selected_module = (
            input("Select desired module (3, 4, 5, 6, or all): ").strip().lower()
        )
        # Check for a valid choice and correct user if not in valid choices.
        if selected_module in {"3", "4", "5", "6", "all"}:
            break
        print("Please enter 3, 4, 5, 6, or all.")

    if selected_module == "all":  # If all selected, search all documents.
        results = collection.query(
            query_texts=[search_text], n_results=5
        )  # n_results=5, return top 5 results
    # otherwise search specified module using where={"module": selected_module}
    else:
        results = collection.query(
            query_texts=[search_text],
            n_results=5,
            where={"module": selected_module},
        )

    # Show distances and metadata
    result_documents = results["documents"]
    result_distances = results["distances"]
    result_metadatas = results["metadatas"]
    if result_documents is None or result_distances is None or result_metadatas is None:
        print("No results found.")
        continue

    for index, doc in enumerate(result_documents[0]):
        distance = result_distances[0][index]
        metadata = result_metadatas[0][index]

        print(
            f"{index + 1}. [distance: {distance:.4f}] "
            f"(Module {metadata['module']}, {metadata['topic']})"
        )
        print(f"   {doc[:100]}...")
        print()

# Explicit test queries

# test_queries = [
#     (
#         "Broad search across all modules",
#         "What topics are covered in this course?",
#         None,
#     ),
#     ("Module 5 filtered search", "How does FastAPI validate incoming data?", "5"),
#     (
#         "Semantic search with different wording",
#         "How can an app remember a person's choices after refreshing?",
#         None,
#     ),
# ]

# for test_name, query_text, module_filter in test_queries:
#     print(f"\n{test_name}: {query_text}")
#     if module_filter is None:
#         test_results = collection.query(query_texts=[query_text], n_results=5)
#     else:
#         test_results = collection.query(
#             query_texts=[query_text],
#             n_results=5,
#             where={"module": module_filter},
#         )

#     test_documents = test_results["documents"]
#     test_metadatas = test_results["metadatas"]
#     if test_documents is None or test_metadatas is None:
#         print("No results found.")
#         continue

#     for index, doc in enumerate(test_documents[0]):
#         metadata = test_metadatas[0][index]
#         print(f"{index + 1}. (Module {metadata['module']}, {metadata['topic']})")
#         print(f"   {doc[:100]}...")
