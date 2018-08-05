#include <pcap.h> 
#include <string.h> 
#include <stdlib.h> 
#include <stdint.h>
#include <ctype.h>

#include <amqp.h>
#include <amqp_tcp_socket.h>

#include "amqp-utils.h"


#define MAXBYTES2CAPTURE 4096
#define SUMMARY_EVERY_US 1000000
#define EXCHANGE "capture"
#define EXCHANGE_TYPE "topic"


// open connection with RabbitMQ server
amqp_connection_state_t createRabbitMQConnection(char *hostname, int port){

    int status;
    amqp_socket_t *socket = NULL;
    amqp_connection_state_t conn;

    conn = amqp_new_connection();

    socket = amqp_tcp_socket_new(conn);
    if (!socket) {
        die("creating TCP socket");
    }

    status = amqp_socket_open(socket, hostname, port);
    if (status) {
        die("opening TCP socket");
    }

    die_on_amqp_error(amqp_login(conn, "/", 0, 131072, 0, AMQP_SASL_METHOD_PLAIN,
                                 "guest", "guest"),
                      "Logging in");
    
    amqp_channel_open(conn, 1);
    die_on_amqp_error(amqp_get_rpc_reply(conn), "Opening channel");

    amqp_exchange_declare(conn, 1, amqp_cstring_bytes(EXCHANGE), 
                          amqp_cstring_bytes(EXCHANGE_TYPE), 0, 0, 0, 0,
                          amqp_empty_table);

    die_on_amqp_error(amqp_get_rpc_reply(conn), "Declaring exchange");

    return conn;

}


// packet processing
void packetHandler(u_char *arg, const struct pcap_pkthdr* pkthdr, const u_char * packet){ 

    amqp_connection_state_t conn = (amqp_connection_state_t)arg;

    /*for (i=0; i<pkthdr->len; i++){ 

    if ( isprint(packet[i]) ) // If it is a printable character, print it
        printf("%c ", packet[i]); 
    else 
        printf(". "); 

     if( (i%16 == 0 && i!=0) || i==pkthdr->len-1 ) 
        printf("\n"); 
    } */

    amqp_bytes_t message_bytes;
    message_bytes.len = pkthdr->len;
    message_bytes.bytes = (u_char *)packet;
    
    char *routing_key = "if_name.type.subtype";

    die_on_error(amqp_basic_publish(conn, 1, amqp_cstring_bytes(EXCHANGE),
                                    amqp_cstring_bytes(routing_key), 0, 0, NULL,
                                    message_bytes),
                 "Publishing");

    return; 

} 


int main(int argc, char *argv[] ){ 

    int i=0, port=5672; 
    pcap_t *handle= NULL; 
    char errbuf[PCAP_ERRBUF_SIZE], *dev=NULL, *hostname = "localhost"; 
    memset(errbuf,0,PCAP_ERRBUF_SIZE); 
    amqp_connection_state_t conn;


    if (argc < 2) {
        fprintf(stderr,
                "Usage: eewids-cap device [host] [port]\n");
        return 1;
    }
    dev = argv[1]; // take device from user input

    if (argc > 2)
        hostname = argv[2];
    if (argc == 4)
        port = atoi(argv[3]);

    conn = createRabbitMQConnection(hostname, port);

    printf("Opening device %s\n", dev); 
    
    // TODO not working yet (segfault), but main structure for filtering options
    /*struct bpf_program fp;
    bpf_u_int32 netp;
    char *filter = "";
    if(pcap_compile(handle,&fp,filter,0,netp)==-1) // -1 means failed
        fprintf(stderr,"Error compiling Libpcap filter, %s\n",filter);

    if(pcap_setfilter(handle,&fp)==-1) // -1 means failed - but we don't exit(1)
        fprintf(stderr,"Error setting Libpcap filter, %s\n",filter); // same as above*/


    /* Open device in promiscuous mode */ 
    if ( (handle = pcap_open_live(dev, MAXBYTES2CAPTURE, 1, 1000, errbuf)) == NULL){
        fprintf(stderr, "Couldn't open device %s: %s\n", dev, errbuf);
        exit(1);
    }

    /* Loop forever & call packetHandler() for every received packet*/ 
    if ( pcap_loop(handle, -1, packetHandler, (u_char *)conn) == -1){
        fprintf(stderr, "ERROR: %s\n", pcap_geterr(handle) );
        exit(1);
    }

    die_on_amqp_error(amqp_channel_close(conn, 1, AMQP_REPLY_SUCCESS),
                      "Closing channel");
    die_on_amqp_error(amqp_connection_close(conn, AMQP_REPLY_SUCCESS),
                      "Closing connection");
    die_on_error(amqp_destroy_connection(conn), "Ending connection");

    return 0; 

} 

