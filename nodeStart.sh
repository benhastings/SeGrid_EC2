#/bin/bash
sleep 10

sudo xvfb-run --server-args='+extension RANDR -screen 0 1280x800x24' java -jar /home/ubuntu/selenium-server.jar -role node -browser browserName=chrome,maxInstances=9 -maxSession 9 -port 4320 -hub http://seGrid-714528302.us-east-1.elb.amazonaws.com/grid/register -registerCycle 5000 &
