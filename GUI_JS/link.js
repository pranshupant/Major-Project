function link(v1, v2) {
this.front = v1;
this.back = v2;

this.connect = function (link1, link2) {
    this.front = link2.back;
    this.back = link1.front;
}
this.show =  () {
    fill(255);
    line(this.front.x, this.front.y, this.back.x, this.back.y);
}
this.updatefront = function () {
    this.front.x = mouseX;
    this.front.y = mouseY;
}
this.updateback = function () {
    this.back.x = mouseX;
    this.back.y = mouseY;

}
