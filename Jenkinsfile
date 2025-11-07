properties([
    parameters([
        booleanParam(name: 'Checkout', defaultValue: true, description: 'Run Build Stage'),
        booleanParam(name: 'Sonar', defaultValue: false, description: 'Run Test Stage'),
        booleanParam(name: 'Dockerbuild', defaultValue: true, description: 'Run Deploy Stage'),
        booleanParam(name: 'Scan', defaultValue: false, description: 'Run Deploy Stage'),
        booleanParam(name: 'Sbom', defaultValue: false, description: 'Run Deploy Stage'),
        booleanParam(name: 'Deploy', defaultValue: true, description: 'Run Deploy Stage')
   
    ])
])


def APP_VERSION='latest'
def SONAR_PROJECT= ''
podTemplate(yaml: """
apiVersion: v1
kind: Pod
metadata:
  labels:
    some-label: jenkins-agent    
spec:
  nodeSelector:
    beta.kubernetes.io/arch: amd64
  serviceAccountName: jenkins-sa  
  containers:
  - name: jnlp
    image: jenkins/inbound-agent
  - name: sonar
    image: sonarsource/sonar-scanner-cli:latest
    command:
    - cat
    tty: true
  - name: buildah
    image: quay.io/buildah/stable
    command:
    - cat
    tty: true
    securityContext:
      privileged: true
  - name: trivy
    image: aquasec/trivy
    command:
    - cat
    tty: true
  - name: syft
    image: mohitsaluja/custom-syft:amd64
    command:
    - cat
    tty: true
  - name: kubectl
    image: mohitsaluja/kubectl:1.29.0
    command:
      - cat
    tty: true

""") {
    node(POD_LABEL) {

    def branchName = env.GIT_BRANCH

    if (branchName == "development") {
           SONAR_PROJECT == "ci.mohitsaluja.blog"
           NAMESPACE = "website-ci"}

    else
        {
           SONAR_PROJECT == "www.mohitsaluja.blog"
           NAMESPACE = "website"
        }

     if (params.Checkout == true ) {
        stage('Checkout') {
      
        withCredentials([string(credentialsId: 'github-secret', variable: 'TOKEN')]) {
                    sh 'git clone -b development https://$TOKEN@github.com/mohitsaluja80/blog.git'
                
            
        }
        

        }
       }
    
        if (params.Sonar == true ) {
                Checkout = true
        stage('Sonar Scan') {
            echo "Sonar Project name is $SONAR_PROJECT"
         
            
            container('sonar') {
                 withCredentials([string(credentialsId: 'sonar-token', variable: 'SONAR')]) {
                withSonarQubeEnv('SonarQube') {  // Name configured in Jenkins
                    sh '''
                    ${SONAR_SCANNER_HOME}/bin/sonar-scanner \
                        -Dsonar.projectKey=ci.mohitsaluja.blog \
                        -Dsonar.sources=. \
                        -Dsonar.host.url=http://sonarqube-sonarqube.sonarqube:9000 \
                        -Dsonar.login=$SONAR
                    '''
                }   
            }
            }
        }
        }
        
    
    
    
    if (params.Dockerbuild == true ) {
        
        stage('build image') {
        

                container(name: 'buildah') {
                   withCredentials([usernamePassword(credentialsId: 'dockerhub', passwordVariable: 'pass', usernameVariable: 'user')]) {
                     sh "buildah login -u $user -p $pass docker.io/mohitsaluja"
                     sh "ls $workspace"
                     sh "ls"
                     //sh "buildah build --layers --cache-to mohitsaluja/cache --cache-from mohitsaluja/cache -t mohitsaluja/myapp:${APP_VERSION} $workspace/blog/Dockerfile"
                     sh "buildah build -t mohitsaluja/myapp:${APP_VERSION} $workspace/blog/Dockerfile"

                     sh "buildah push  mohitsaluja/myapp:${APP_VERSION}"
                   }
         
                }
            }
        }
        
    
    
    
    if (params.Scan == true ) {
        stage('Vulnerability Scan') {
        container(name: 'trivy') {
         withCredentials([usernamePassword(credentialsId: 'dockerhub', passwordVariable: 'pass', usernameVariable: 'user')]) {
                sh "trivy image --username $user --password $pass --format json --output result.json mohitsaluja/myapp:${APP_VERSION}"
                archiveArtifacts artifacts: 'result.json', followSymlinks: false
            
              }
        }
        }  
    }
    
    
    if (params.Sbom == true ) {
         
        stage('Generating SBOM') {
        container(name: 'syft') {
         withCredentials([usernamePassword(credentialsId: 'dockerhub', passwordVariable: 'pass', usernameVariable: 'user')]) {
                sh "syft login docker.io -u $user -p $pass"
                sh "syft scan mohitsaluja/myapp:${APP_VERSION} -o spdx-json --file sbom.json"
                archiveArtifacts artifacts: 'sbom.json', followSymlinks: false
            
              }
        }
            
        }   
        
    }

      if (params.Deploy == true ) {
          echo "Namespace name is $NAMESPACE"
         
        stage('Deploying new release') {
        container(name: 'kubectl') {
             
                 sh "kubectl rollout restart deployment website-ci -n ${NAMESPACE}"
              }
           
              
        }
            
        }   
        
    }


  }
