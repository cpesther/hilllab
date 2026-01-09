// Christopher Esther, Hill Lab, 12/18/2025
using System.Numerics;
using MathNet.Numerics.IntegralTransforms;
using OpenCvSharp;

namespace FFTProcessor
{
    class Program
    {
        static void Main(string[] args)
        {
            try
            {
                Console.WriteLine("FFTProcessor.exe launched");

                // Argument check
                if (args.Length != 6)
                {
                    Console.WriteLine("Usage: FFTProcessor <videoPath> <psdFile> <freqFile> <metaPath> <samplingRate> <showPrint>");
                    return;
                }

                string videoPath = args[0];
                string psdFile = args[1];
                string freqFile = args[2];
                string metaPath = args[3];
                float samplingRate = float.Parse(args[4]);
                bool showPrint = bool.Parse(args[5]);

                // Check that the video path exists
                if (!File.Exists(videoPath))
                {
                    Console.WriteLine($"ERROR: Video file not found: {videoPath}");
                    return;
                }

                // Open the video capture object
                using var cap = new VideoCapture(videoPath);
                if (!cap.IsOpened())
                {
                    Console.WriteLine($"ERROR: Cannot open video {videoPath}");
                    return;
                }

                // Some basic calculations
                int frameWidth = (int)cap.Get(VideoCaptureProperties.FrameWidth);
                int frameHeight = (int)cap.Get(VideoCaptureProperties.FrameHeight);
                int maxFrames = (int)cap.Get(VideoCaptureProperties.FrameCount);

                if (showPrint) {Console.WriteLine($"Video opened: {frameWidth}x{frameHeight}, up to {maxFrames} frames");}

                // Allocate using reported frame count
                if (showPrint) {Console.WriteLine("Converting video to grayscale...");}
                byte[,,] tempFrames = new byte[maxFrames, frameHeight, frameWidth];

                using Mat frame = new Mat();
                using Mat gray = new Mat();

                int frameIndex = 0;  // actual number of frames read

                while (cap.Read(frame))
                {
                    if (frame.Empty())
                        break;

                    Cv2.CvtColor(frame, gray, ColorConversionCodes.BGR2GRAY);

                    for (int y = 0; y < frameHeight; y++)
                        for (int x = 0; x < frameWidth; x++)
                            tempFrames[frameIndex, y, x] = gray.At<byte>(y, x);

                    frameIndex++;
                }

                // IMPORTANT: use the actual frame count
                int numFrames = frameIndex;

                // Resize to exact size actually read
                byte[,,] grayscaleFrames = new byte[numFrames, frameHeight, frameWidth];
                Array.Copy(
                    tempFrames,
                    grayscaleFrames,
                    numFrames * frameHeight * frameWidth
                );

                if (showPrint) {Console.WriteLine($"Finished converting {numFrames} frames");}

                int fftLength = numFrames / 2 + 1;
                float[] psdMap = new float[frameHeight * frameWidth * fftLength];
                float[] freqMap = new float[frameHeight * frameWidth];

                int totalPixels = frameHeight * frameWidth;
                int rowsCompleted = 0;

                if (showPrint) {Console.WriteLine("Starting FFT processing");}

                // Run the FFT on every pixel in time series
                Parallel.For(0, frameHeight, row =>
                {
                    for (int col = 0; col < frameWidth; col++)
                    {
                        // Pull the time series values for this pixel into ts
                        Complex[] ts = new Complex[numFrames];
                        double mean = 0.0;

                        for (int f = 0; f < numFrames; f++)
                        {
                            float val = grayscaleFrames[f, row, col];
                            mean += val;
                            ts[f] = new Complex(val, 0);
                        }

                        // Calculate mean value and normalize time series
                        mean /= numFrames;
                        for (int f = 0; f < numFrames; f++)
                            ts[f] -= mean;

                        // The actual FFT
                        Fourier.Forward(ts, FourierOptions.Matlab);

                        double maxPower = 0.0;
                        int maxIndex = 0;
                        // Iterate through the FFT results to calculate the power and record its maximum
                        for (int i = 0; i < fftLength; i++)
                        {
                            double power = (ts[i].Magnitude * ts[i].Magnitude) / (numFrames * samplingRate);

                            if (i > 0 && i < fftLength - 1)
                                power *= 2;

                            if (i < 15)
                                power = 0;

                            psdMap[row * frameWidth * fftLength + col * fftLength + i] = (float)power;

                            if (power > maxPower)
                            {
                                maxPower = power;
                                maxIndex = i;
                            }
                        }

                        // Save the frequency value associated with the maximum power
                        freqMap[row * frameWidth + col] =
                            (float)maxIndex * samplingRate / numFrames;
                    }

                    int doneRows = System.Threading.Interlocked.Increment(ref rowsCompleted);
                    if (showPrint) {Console.WriteLine($"Processed {doneRows * frameWidth} / {totalPixels} pixels");}
                });

                if (showPrint) {Console.WriteLine("Finished FFT. Saving results...");}

                // Write the PSD and frequency maps to binary files
                using (var fs = new FileStream(psdFile, FileMode.Create))
                using (var bw = new BinaryWriter(fs))
                    for (int i = 0; i < psdMap.Length; i++)
                        bw.Write(psdMap[i]);

                using (var fs = new FileStream(freqFile, FileMode.Create))
                using (var bw = new BinaryWriter(fs))
                    for (int i = 0; i < freqMap.Length; i++)
                        bw.Write(freqMap[i]);

                // And write the metadata to a little text file
                File.WriteAllLines(metaPath, new[]
                {
                    numFrames.ToString(),
                    frameHeight.ToString(),
                    frameWidth.ToString()
                });

                if (showPrint) {Console.WriteLine("FFT processing completed!");}
            }
            catch (Exception ex)
            {
                Console.WriteLine("Unhandled exception:");
                Console.WriteLine(ex);
            }
        }
    }
}
