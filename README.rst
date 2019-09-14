==================
Valgreen
==================

.. image:: https://badge.fury.io/py/valgreen.svg
    :target: https://badge.fury.io/py/valgreen

Valgrind output readable for human beings

With *Valgreen*:

.. image:: https://i.imgur.com/V0XrzXp.gif
    :target: https://asciinema.org/a/268317

With *Valgrind*:

.. image:: https://i.imgur.com/rVXnlEB.gif
    :target: https://asciinema.org/a/vnZy9cmp3VbkPhPzwfoGBRGlB

Installation
============

As simple as :code:`pip3 install valgreen`. Keep in mind you need a working Valgrind installation!

Usage
=====

Just write :code:`valgreen ./exec` instead of :code:`valgrind --leak-check=full --track-origins=yes --show-reachable=yes ./exec`

Example
=======

Valgreen vs Valgrind output

.. code::

    $ gcc -g example.c -o example
    $ valgreen ./example

     1) Conditional jump or move depends on uninitialised value(s)
       at main (example.c:8)
       Uninitialised value was created by a stack allocation
       at main (example.c:4)

     2) Invalid write of size 1
       at main (example.c:12)
        Address 0x522d042 is 0 bytes after a block of size 2 alloc'd
        at malloc (in /usr/lib/valgrind/vgpreload_memcheck-amd64-linux.so)
        by main (example.c:11)

     3) Invalid read of size 1
       at main (example.c:15)
        Address 0x522d045 is 3 bytes after a block of size 2 alloc'd
        at malloc (in /usr/lib/valgrind/vgpreload_memcheck-amd64-linux.so)
        by main (example.c:11)

     4) Invalid free() / delete / delete[] / realloc()
       at free (in /usr/lib/valgrind/vgpreload_memcheck-amd64-linux.so)
        by main (example.c:19)
       Address 0x522d040 is 0 bytes inside a block of size 2 free'd
       at free (in /usr/lib/valgrind/vgpreload_memcheck-amd64-linux.so)
        by main (example.c:18)
       Block was alloc'd at
       at malloc (in /usr/lib/valgrind/vgpreload_memcheck-amd64-linux.so)
        by main (example.c:11)

     5) 100 bytes in 1 blocks are definitely lost in loss record 1 of 1
       at malloc (in /usr/lib/valgrind/vgpreload_memcheck-amd64-linux.so)
        by main (example.c:22)

    $ valgrind --leak-check=full --track-origins=yes --show-reachable=yes ./example 

    ==7750== Memcheck, a memory error detector
    ==7750== Copyright (C) 2002-2017, and GNU GPL'd, by Julian Seward et al.
    ==7750== Using Valgrind-3.13.0 and LibVEX; rerun with -h for copyright info
    ==7750== Command: ./example
    ==7750== 
    ==7750== Conditional jump or move depends on uninitialised value(s)
    ==7750==    at 0x108696: main (example.c:8)
    ==7750==  Uninitialised value was created by a stack allocation
    ==7750==    at 0x10868A: main (example.c:4)
    ==7750== 
    ==7750== Invalid write of size 1
    ==7750==    at 0x1086B5: main (example.c:12)
    ==7750==  Address 0x522d042 is 0 bytes after a block of size 2 alloc'd
    ==7750==    at 0x4C2FB0F: malloc (in /usr/lib/valgrind/vgpreload_memcheck-amd64-linux.so)
    ==7750==    by 0x1086A8: main (example.c:11)
    ==7750== 
    ==7750== Invalid read of size 1
    ==7750==    at 0x1086BC: main (example.c:15)
    ==7750==  Address 0x522d045 is 3 bytes after a block of size 2 alloc'd
    ==7750==    at 0x4C2FB0F: malloc (in /usr/lib/valgrind/vgpreload_memcheck-amd64-linux.so)
    ==7750==    by 0x1086A8: main (example.c:11)
    ==7750== 
    ==7750== Invalid free() / delete / delete[] / realloc()
    ==7750==    at 0x4C30D3B: free (in /usr/lib/valgrind/vgpreload_memcheck-amd64-linux.so)
    ==7750==    by 0x1086DA: main (example.c:19)
    ==7750==  Address 0x522d040 is 0 bytes inside a block of size 2 free'd
    ==7750==    at 0x4C30D3B: free (in /usr/lib/valgrind/vgpreload_memcheck-amd64-linux.so)
    ==7750==    by 0x1086CE: main (example.c:18)
    ==7750==  Block was alloc'd at
    ==7750==    at 0x4C2FB0F: malloc (in /usr/lib/valgrind/vgpreload_memcheck-amd64-linux.so)
    ==7750==    by 0x1086A8: main (example.c:11)
    ==7750== 
    ==7750== 
    ==7750== HEAP SUMMARY:
    ==7750==     in use at exit: 100 bytes in 1 blocks
    ==7750==   total heap usage: 2 allocs, 2 frees, 102 bytes allocated
    ==7750== 
    ==7750== 100 bytes in 1 blocks are definitely lost in loss record 1 of 1
    ==7750==    at 0x4C2FB0F: malloc (in /usr/lib/valgrind/vgpreload_memcheck-amd64-linux.so)
    ==7750==    by 0x1086E4: main (example.c:22)
    ==7750== 
    ==7750== LEAK SUMMARY:
    ==7750==    definitely lost: 100 bytes in 1 blocks
    ==7750==    indirectly lost: 0 bytes in 0 blocks
    ==7750==      possibly lost: 0 bytes in 0 blocks
    ==7750==    still reachable: 0 bytes in 0 blocks
    ==7750==         suppressed: 0 bytes in 0 blocks
    ==7750== 
    ==7750== For counts of detected and suppressed errors, rerun with: -v
    ==7750== ERROR SUMMARY: 5 errors from 5 contexts (suppressed: 0 from 0)