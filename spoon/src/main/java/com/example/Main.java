package com.example;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

import spoon.Launcher;
import spoon.reflect.CtModel;
import spoon.reflect.declaration.CtType;

public class Main {

    public static void main(String[] args) throws IOException {
        String projectFilesText = args[0];
        String diffFilesText = args[1];
        String outPutFile = args[2];
        
        String allFilesString = getAllFiles(projectFilesText);
        allFilesString = allFilesString.replace("\r\n", "\n");
        String[] modulesFiles = allFilesString.split("\n\n");

        List<String> diffFiles = getdiffFiles(diffFilesText);
        List<Path> diffFilesPath = diffFiles.stream()
                .map(a -> Paths.get(a))
                .filter(a -> Files.exists(a))
                .toList();//変更ファイルを入手
        Visitor visitor = new Visitor();

        for (String moduleFiles : modulesFiles) {
            String[] tmp = moduleFiles.split("\n");
            List<String> ListModuleFiles = Arrays.asList(tmp);
            List<Path> ListModuleFilesPath=ListModuleFiles.stream().map(a->Paths.get(a)).filter(a->Files.exists(a)).toList();
            for (Path diffFilePath : diffFilesPath) {
                if (ListModuleFilesPath.contains(diffFilePath)) {
                    Launcher launcher = new Launcher();
                    ListModuleFiles.forEach(a -> launcher.addInputResource(a));
                    launcher.getEnvironment().setCommentEnabled(false);
                    launcher.getEnvironment().setAutoImports(true);
                    CtModel model = launcher.buildModel();

                    for (CtType<?> clazz : model.getAllTypes()) {

                        if (clazz.getPosition().getFile() != null && diffFilesPath.contains(Paths.get(clazz.getPosition().getFile().getAbsolutePath()))) {
                            clazz.accept(visitor);
                        }
                    }
                    break;
                }
            }
        }
        visitor.printCSV(outPutFile);

    }

    public static List<String> getdiffFiles(String path) {
        try {
            File File = new File(path);   //後ほどlogを読み取ったファイルに置き換える
            List<String> FileList;
            try (BufferedReader Reader = new BufferedReader(new FileReader(File))) {
                FileList = new ArrayList<>();
                String str;
                while ((str = Reader.readLine()) != null) {
                    FileList.add(str);                                          //１つ目の要素はgitのhash値　それ以降の要素が変更のあったファイル名
                }
            }
            return FileList;
        } catch (IOException e) {
            System.out.println(e);
        }
        return null;
    }

    public static String getAllFiles(String path) {
        try {
            File file = new File(path);
            String allString;
            try (BufferedReader Reader = new BufferedReader(new FileReader(file))) {
                int str;
                allString = "";
                while ((str = Reader.read()) != -1) {
                    allString = allString + (char) str;
                }
            }
            return allString;
        } catch (IOException e) {
            System.out.println(e.getMessage());
            return null;
        }
    }
}

/*  
        try {
            File allfile = new File("c:\\Users\\sugii syuji\\spoonTEXT\\demo\\first.txt");
            BufferedReader allreader = new BufferedReader(new FileReader(allfile));
            String str;
            while ((str = allreader.readLine()) != null) {
                launcher.addInputResource(str);
            }
            allreader.close();
        } catch (IOException e) {
            System.out.println(e);
        }
private static List<String> addJarSourceFile(Path path) throws IOException {
        List<String> JarFile;
        try (Stream<Path> paths = Files.walk(path)) {
            JarFile = paths.filter(p -> p.toString().endsWith(".jar")).map(p -> p.toString()).toList();
        }
        return JarFile;
    }

}
   
    //JarFile=filterConflictingJars(JarFile);
    private static List<String> filterConflictingJars(List<String> jars) {
        List<String> safe = new ArrayList<>();
        for (String jar : jars) {
            try (JarFile jf = new JarFile(jar)) {
                boolean hasConflict = jf.stream().anyMatch(entry -> {
                    String name = entry.getName();
                    return name.startsWith("org/w3c/dom")
                            || name.startsWith("javax/xml/")
                            || name.startsWith("org/xml/sax/");
                });
                if (!hasConflict) {
                    safe.add(jar);
                } else {
                    System.out.println("Conflict : " + jar);
                }
            } catch (Exception e) {
            }
        }
        return safe;
    }*/
