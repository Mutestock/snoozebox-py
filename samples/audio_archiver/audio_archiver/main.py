import multiprocessing

from service.frontend.flask_templates import run_templates
from service.grpc.grpc_main import run_grpc
from connection.pg_connection import db_init



# Uses threading to start both the flask jinja templates, as well as the gRPC service.
# It's sort of questionable whether or not that's a good idea, but eh.

def main() -> None:
    db_init()
    
    flask_process = multiprocessing.Process(target=run_templates)
    grpc_process = multiprocessing.Process(target=run_grpc)
    
    print("Starting templates...")
    flask_process.start()
    
    print("Starting grpc...")
    grpc_process.start()
    
    print("Running...")
    flask_process.join()
    
    print("Templates aborted. Waiting for signal to terminate grpc process...")
    grpc_process.join()
    
    print("Both processes aborted...")
    print("finished")
    

if __name__ == "__main__":
    main()
    