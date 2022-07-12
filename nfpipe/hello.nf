#!/usr/bin/env nextflow
nextflow.enable.dsl=2 

process sayHello {
    cpus 1
    memory '2GB'
    time '10m'
    queue 'debug' 

    input: 
        val x
    output:
        stdout
    script:
        """
        echo '$x world!'
        """
}

workflow {
  Channel.of('Bonjour', 'Ciao', 'Hello', 'Hola') | sayHello | view
}