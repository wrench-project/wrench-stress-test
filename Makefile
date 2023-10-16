.NOTPARALLEL:


TO_EXCLUDE = 1.0 1.1 1.2 1.3 1.4 1.5 1.6 1.7 1.8 1.9 1.10 1.11 2.0 

COMMAND = find ./Dockerfiles -name 'Dockerfile_*' $(foreach version, $(TO_EXCLUDE), -not -name 'Dockerfile_*$(version)')
DOCKERFILES := $(shell $(COMMAND))
IMAGENAMES := $(shell echo $(DOCKERFILES) | sed "s/\.\/Dockerfiles\/Dockerfile_wrench_stress_test_/wrench_benchmark_/g")


default:
	@echo "make build: will build the Docker containers and the simulators (do this first)"


build:
	@for dockerfile in ${DOCKERFILES} ; do \
	echo "*********" ; \
    	echo "** Building Docker image for $${dockerfile} **" ; \
	echo "*********" ; \
	image_name=wrench_benchmark_`echo $${dockerfile} | sed "s/.*test_//"` ; \
	echo docker build -t $${image_name} -f $${dockerfile} . ; \
	docker build -t $${image_name} -f $${dockerfile} . ; \
	done	


run:
	@./run_all_containers.py ${IMAGENAMES}


