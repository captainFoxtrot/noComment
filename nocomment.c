#include        <stdio.h>
#include        <stdint.h>
#include        <stdlib.h>

#define         MEMORYSIZE      10000
#define         STACKSIZE       10000

FILE*           f;
uint8_t*        memory;
uint8_t*        memptr;
uint8_t*        stackbase;
uint8_t*        stackptr;
char            ch;

int main(const int argc, const char** argv){

        // Exit if no filename provided
        if(argc == 1){
                printf("Enter a filename to run.\n");
                return 1;
        }

        // Exit if the file could not be opened
        if(!(f = fopen(argv[1], "r"))){
                printf("Unable to open file \"%s\".\n", argv[1]);
                return 1;
        }

        // Allocate memory for the memory space and stack
        memory    = memptr   = (uint8_t*) calloc(MEMORYSIZE, sizeof(uint8_t));
        stackbase = stackptr = (uint8_t*) calloc(STACKSIZE,  sizeof(uint8_t));

        // Print error message and exit if memory space allocation failed
        if(!memory)
                goto allocationerror;

        // Print error message and exit if stack allocation failed
        if(!stackbase)
                goto allocationerror;

        while(1){
                // Get the next character in the file
                ch = fgetc(f);

                // Exit loop if end of file
                if(feof(f))
                        break;
                
                // 
                switch(ch){

                        // Increment value of pointer
                        case 'i':
                                ++*memptr;
                                break;

                        // Decrement value of pointer
                        case 'd':
                                --*memptr;
                                break;

                        // Clear (zero) value of pointer
                        case 'c':
                                *memptr = 0;
                                break;

                        // Decrement pointer
                        case 'l':
                                --memptr;

                                // Wrap-around if pointer underflow
                                if(memptr < memory)
                                        memptr += MEMORYSIZE;
                                break;

                        // Increment pointer
                        case 'r':
                                ++memptr;

                                // Wrap-around if pointer overflow
                                if((int)memory + MEMORYSIZE == (int)memptr)
                                        memptr = memory;
                                break;

                        // Push value of pointer to stack
                        case 'n':
                                // Put the ptr val on stack
                                *stackptr = *memptr;

                                // Increment stack pointer
                                ++stackptr;

                                break;

                        // Pop from stack to value of pointer
                        case 'f':
                                // Decrement stack pointer
                                --stackptr;

                                // Override ptr val with stack
                                *memptr = *stackptr;

                                break;

                        // Forward jump if non-zero value of pointer
                        case 's':
                                if(*memptr)
                                        fseek(f, *(stackptr - 1), SEEK_CUR);
                                break;

                        // Backwards jump if non-zero value of pointer
                        case 'b':
                                if(*memptr)
                                        fseek(f, -*(stackptr - 1), SEEK_CUR);
                                break;

                        // Print value of pointer as ASCII char
                        case 'o':
                                putchar(*memptr);
                                break;

                        // Unknown instruction
                        default:
                                printf("Illegal instruction %i at character %li.\n", ch, ftell(f));
                                return 1;
                }
        }

        // Close the file and deallocate memory
        fclose(f);
        free(memory);
        free(stackbase);

        // Exit
        return 0;

        allocationerror:
                printf("Unable to allocate memory.\n");
                return 1;
}
