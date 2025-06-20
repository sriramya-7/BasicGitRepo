pipeline {
    agent any
    environment {
        KUBECONFIG = "${env. KUBECONFIG}"
        BRANCH_NAME = "${env.BRANCH_NAME}"
        REPO_URL = "${env.REPO_URL}"
        K8S_REPO_URL = "${env.K8S_REPO_URL}"
        K8S_REPO_BRANCH_NAME = "${env.K8S_REPO_BRANCH_NAME}"
        DOCKER_HUB_USERNAME = "${env.DOCKER_HUB_USERNAME}"
        DOCKER_HUB_TAGNAME = "${env.DOCKER_HUB_TAGNAME}"
        DOCKER_IMAGE = "${env.DOCKER_IMAGE}"
        CONTAINER_NAME = "${env.CONTAINER_NAME}"
        MANIFESTO_BRANCH_NAME = "${env.MANIFESTO_BRANCH_NAME}"
        K8S_REPO_FOLDER_NAME = "${env.K8S_REPO_FOLDER_NAME}"
    }
    
    stages {
        stage('Checkout Code') {
            steps {
                git branch: "${env.BRANCH_NAME}",
                    url: "${env.REPO_URL}"
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                    docker build -t ${DOCKER_IMAGE} .
                    docker tag ${DOCKER_IMAGE} ${DOCKER_HUB_USERNAME}/${DOCKER_HUB_TAGNAME}:${DOCKER_IMAGE}
                '''
            }
        }

        stage('Push Docker Image to Docker Hub') {
            steps {
                withCredentials([string(credentialsId: 'DOCKER_HUB_PASSWORD', variable: 'DOCKER_HUB_PASS')]) {
                    sh '''
                        echo "$DOCKER_HUB_PASS" | docker login -u ${DOCKER_HUB_USERNAME} --password-stdin
                        docker push ${DOCKER_HUB_USERNAME}/${DOCKER_HUB_TAGNAME}:${DOCKER_IMAGE}
                    '''
                }
            }
        }

        stage('checkout kubernetes Manifests') {
            steps {
                git branch: "${MANIFESTO_BRANCH_NAME}",
                    url: "${K8S_REPO_URL}"
            }
        }

        stage('Update Minikube Context') {
            steps {
                sh '''
                export KUBECONFIG="C:/Users/dhira/.kube/config"
                minikube update-context
            '''
            }
        }
        
        stage('Check Cluster Info') {
            steps {
                  sh '''
                export KUBECONFIG="C:/Users/dhira/.kube/config"
                kubectl cluster-info
            '''
            }
        }

        stage('Check Minikube') {
            steps {
                sh '''
                    which minikube
                    minikube version
                    minikube status
                '''
            }
        }

        stage('Start Minikube') {
            steps {
                script {
                    def minikubeStatus = sh(script: 'minikube status || echo "Stopped"', returnStdout: true).trim()
                    if (!minikubeStatus.contains("Running")) {
                        sh '''
                            minikube start --driver=docker
                            minikube addons enable ingress
                        '''
                    } else {
                        echo "Minikube is already running."
                    }
                }
            }
        }
        // checkin
        stage('Deploy to Minikube') {
            steps {
                sh '''
                    kubectl apply -f configmap.yaml
                    kubectl apply -f deployment.yaml
                    kubectl apply -f service.yaml
                    kubectl apply -f ingress.yaml
                '''
            }
        }

        stage('Verify Deployment') {
            steps {
                sh '''
                    echo "Checking pods..."
                    kubectl get pods -o wide
                    echo "Checking services..."
                    kubectl get svc
                    echo "Checking ingress..."
                    kubectl get ingress
                '''
            }
        }
    }

    post {
        success {
            echo 'Deployment success'
        }
        failure {
            echo 'Deployment failure'
        }
    }
}
