saveButton = ButtonLabel(
    #         self,
    #         text="Save",
    #         command=self.saveHSVdata
    #     )
    #     saveButton.pack(pady=5, padx=10, side="bottom")

    #     h_minLabel = TextLabel(self,
    #                            text="HUE Min",
    #                            )
    #     h_minLabel.pack()
    #     h_min = SliderLabel(self, from_=0, to=180,
    #                         resolution=1,
    #                         command=self.updateVideoFeeds
    #                         )
    #     h_min.set(0)
    #     h_min.pack()
    #     self.h_min = h_min

    #     h_maxLabel = TextLabel(self,
    #                            text="HUE Max",
    #                            )
    #     h_maxLabel.pack()
    #     h_max = SliderLabel(self, from_=0, to=180,
    #                         resolution=1,
    #                         command=self.updateVideoFeeds
    #                         )
    #     h_max.set(180)
    #     h_max.pack()
    #     self.h_max = h_max

    #     s_minLabel = TextLabel(self,
    #                            text="SAT Min",
    #                            )
    #     s_minLabel.pack()
    #     s_min = SliderLabel(self, from_=0, to=255,
    #                         resolution=1,
    #                         command=self.updateVideoFeeds
    #                         )
    #     s_min.set(0)
    #     s_min.pack()
    #     self.s_min = s_min

    #     s_maxLabel = TextLabel(self,
    #                            text="SAT Max",
    #                            )
    #     s_maxLabel.pack()
    #     s_max = SliderLabel(self, from_=0, to=255,
    #                         resolution=1,
    #                         command=self.updateVideoFeeds
    #                         )
    #     s_max.set(255)
    #     s_max.pack()
    #     self.s_max = s_max

    #     v_minLabel = TextLabel(self,
    #                            text="VALUE Min",
    #                            )
    #     v_minLabel.pack()
    #     v_min = SliderLabel(self, from_=0, to=255,
    #                         resolution=1,
    #                         command=self.updateVideoFeeds
    #                         )
    #     v_min.set(0)
    #     v_min.pack()
    #     self.v_min = v_min

    #     v_maxLabel = TextLabel(self,
    #                            text="VALUE Max",
    #                            )
    #     v_maxLabel.pack()
    #     v_max = SliderLabel(self, from_=0, to=255,
    #                         resolution=1,
    #                         command=self.updateVideoFeeds
    #                         )
    #     v_max.set(255)
    #     v_max.pack()
    #     self.v_max = v_max

    # def saveHSVdata(self):
    #     minData = (self.h_min.get(), self.s_min.get(), self.v_min.get())
    #     maxData = (self.h_max.get(), self.s_max.get(), self.v_max.get(),)
    #     print(f"{minData}, {maxData}")

    # def updateVideoFeeds(self, var):
    #     image1, image2 = objectdetector.adjustHSV(
    #         self.h_min.get(),
    #         self.h_max.get(),
    #         self.s_min.get(),
    #         self.s_max.get(),
    #         self.v_min.get(),
    #         self.v_max.get(),
    #     )
    #     image1 = cvtImage(image1)
    #     image2 = cvtImage(image2)
    #     self.image1 = image1
    #     self.image2 = image2
    #     self.videoFeed1.configure(image=self.image1)
    #     self.videoFeed2.configure(image=self.image2)
    #     self.container.update()
