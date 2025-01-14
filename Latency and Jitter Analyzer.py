import cv2
import random
import time

# Simulate packet arrival times
def simulate_packets(total_packets=1000, loss_rate=0.1, max_jitter=50):
    packets = []
    expected_time = 0  # Expected arrival time (ms)

    for i in range(total_packets):
        jitter = random.randint(-max_jitter, max_jitter)

        # Simulate packet loss
        if random.random() < loss_rate:
            packets.append(None)  # Lost packet
        else:
            actual_time = expected_time + jitter
            packets.append(actual_time)

        expected_time += 100  # Increment expected time by 100ms (10 packets/sec)

    return packets

# Calculate latency and jitter
def calculate_latency_and_jitter(packets):
    latencies = []
    jitter_values = []
    last_valid_time = None

    for i, packet_time in enumerate(packets):
        if packet_time is None:
            continue

        expected_time = i * 100
        latency = abs(packet_time - expected_time)
        latencies.append(latency)

        if last_valid_time is not None:
            jitter = abs(packet_time - last_valid_time)
            jitter_values.append(jitter)

        last_valid_time = packet_time

    avg_latency = sum(latencies) / len(latencies) if latencies else 0
    avg_jitter = sum(jitter_values) / len(jitter_values) if jitter_values else 0

    return avg_latency, avg_jitter

# Simulate video playback
def simulate_video_playback(video_path, packets, latency_threshold=100, jitter_threshold=30):
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print("Error: Unable to open video file.")
        return

    frame_count = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret or frame_count >= len(packets):
            break

        packet_time = packets[frame_count]
        if packet_time is None:  # Packet lost
            print(f"Frame {frame_count}: Lost (Skipping frame)")
        else:
            latency = abs(packet_time - frame_count * 100)
            if latency > latency_threshold:
                print(f"Frame {frame_count}: Buffering due to high latency ({latency}ms)")
                time.sleep(0.5)  # Simulate buffering
            elif frame_count > 0 and packets[frame_count - 1] is not None:
                jitter = abs(packet_time - packets[frame_count - 1])
                if jitter > jitter_threshold:
                    print(f"Frame {frame_count}: Stutter due to high jitter ({jitter}ms)")
                    time.sleep(0.2)  # Simulate stutter
            else:
                print(f"Frame {frame_count}: Smooth playback")
                cv2.imshow("Video Playback", frame)
                cv2.waitKey(30)  # Simulate normal playback speed

        frame_count += 1

    cap.release()
    cv2.destroyAllWindows()

# Main script
if __name__ == "__main__":
    video_path = r"C:\Users\Anagha\OneDrive\Desktop\AdaptiveBitRateOptimization\Videos\TOS_1080p.mp4"  # Replace with the path to your video file
    total_packets = 100
    loss_rate = 0.1  # 10% packet loss
    max_jitter = 50  # Max jitter in ms

    print("Simulating packet arrival...")
    packets = simulate_packets(total_packets, loss_rate, max_jitter)
    print("Packet simulation complete.")

    print("\nCalculating latency and jitter...")
    avg_latency, avg_jitter = calculate_latency_and_jitter(packets)
    print(f"Average Latency: {avg_latency:.2f} ms")
    print(f"Average Jitter: {avg_jitter:.2f} ms")

    print("\nSimulating video playback...")
    simulate_video_playback(video_path, packets)



