var gulp = require("gulp");
var sass = require("gulp-sass");
var autoprefixer = require("gulp-autoprefixer");
var plumber = require("gulp-plumber");
var browser = require("browser-sync");
var minify = require("gulp-minify-css");

gulp.task("server", function() {
    browser({
        notify: false,
        proxy: "127.0.0.1:8000"
    });
});

gulp.task("sass", function() {
    gulp.src("kurokumo/static/styles/*.scss")
        .pipe(plumber())
        .pipe(sass())
        .pipe(autoprefixer())
        .pipe(minify())
        .pipe(gulp.dest("kurokumo/static/styles/"))
        .pipe(browser.reload({stream:true}))
});

gulp.task("default", ['server'], function() {
    gulp.watch("kurokumo/static/styles/*.scss", ["sass"]);
});
