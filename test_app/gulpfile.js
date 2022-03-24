// requirements

var gulp = require('gulp');
var del = require('del');
var babel = require('gulp-babel');

gulp.task("babel", function(){
    return gulp.src("./client/scripts/jsx/*.js").
        pipe(babel({
            plugins: ['transform-react-jsx']
        })).
        pipe(gulp.dest("./client/scripts/js/"));
});


gulp.task('del', function () {
  return del(['./client/scripts/js']);
});
