cd ..
mvn spotless:apply
mvn clean package -e -DskipTests
cd scripts
