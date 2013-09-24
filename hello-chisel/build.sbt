
scalaVersion := "2.10.2"

resolvers ++= Seq(
  "scct-github-repository" at "http://mtkopone.github.com/scct/maven-repo"
)

// sourceDirectories in Compile += new File("src")

// scalaSource in Compile := Path.absolute(file(projectdir + "/src"))

scalaSource in Compile := new File("src")

libraryDependencies += "edu.berkeley.cs" %% "chisel" % "2.0.2"
